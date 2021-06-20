from typing import Tuple

import aioredis
from neo4j import Transaction
from pydantic import parse_obj_as

from dataplane import neo4j
from .consts import SESSION_TTL

from .exceptions import DomainError
from .schemas import (
    AnswerModel,
    AnswerResponseModel,
    MultipleChoiceResponse,
    QuestionModel,
    ResultModel,
    ScaleResponse,
    SingleChoiceResponse, SingleChoiceQuestion, MultipleChoiceQuestion, ScaleQuestion, BodySchemaQuestion,
)


async def get_object(search: str) -> AnswerResponseModel:
    def question_query(tx: Transaction):
        get_question_ = """
        {}
        MATCH (q:Question)-[a]->()
        RETURN id(q), q, a, id(a)
        """.format(search)
        return list(tx.run(get_question_))

    result = await neo4j(question_query)
    if len(result) == 0:
        def result_query(tx: Transaction):
            get_result = """
            {}
            MATCH (r:Result) WHERE ID(r) = ID(q)
            RETURN r
            """.format(search)
            return list(tx.run(get_result))

        result = await neo4j(result_query)
        if len(result) == 0:
            raise DomainError("No such question found")

        return parse_obj_as(ResultModel, dict(result[0]["r"]))

    id_ = result[0]["id(q)"]
    q = dict(result[0]["q"])
    answers = []
    for row in result:
        answers.append({"id": row["id(a)"], **dict(row["a"])})

    model = QuestionModel
    q_dict = {"id": id_, **q}
    if q_dict["type"] == "single":
        model = SingleChoiceQuestion
        q_dict["answers"] = answers
    if q_dict["type"] == "multiple":
        model = MultipleChoiceQuestion
        q_dict["answers"] = answers
    elif q_dict["type"] == "scale":
        model = SingleChoiceQuestion
        q_dict["answers"] = [
            {"id": f"{a['min']},{a['max']}", "text": a["description"]}
            for a in answers
        ]
    elif q_dict["type"] == "body":
        model = BodySchemaQuestion

    return parse_obj_as(model, q_dict)


async def get_next_for_answer_id(answer_id: int) -> AnswerResponseModel:
    return await get_object(f"""
    MATCH ()-[a_]->() WHERE ID(a_) = {answer_id}
    MATCH (_)-[a_]->(q)
    """)


async def get_entry_question() -> QuestionModel:
    return await get_object("MATCH (q:Question {entry:true})")


async def get_next_response(
    redis: aioredis.Redis, session_id: str, answer: AnswerModel
) -> AnswerResponseModel:
    last_question_id = await redis.lrange(session_id, -1, -1)
    if last_question_id is None or len(last_question_id) == 0:
        raise DomainError(f"session_id {session_id} does not exist")

    last_question_id = int(last_question_id[0])

    if last_question_id != answer.question_id:
        raise DomainError(f"Last question id was not {answer.question_id}")

    if last_question_id == -1:
        entry_question = await get_entry_question()
        await redis.rpush(session_id, entry_question.id)
        return entry_question

    def raise_for_format():
        raise DomainError(f"Invalid response format: {type(answer)}")

    last_question = await get_object(f"MATCH (q) WHERE ID(q) = {last_question_id}")
    if last_question.type in ("single", "body"):
        if not isinstance(answer, SingleChoiceResponse):
            raise_for_format()
        next_ = await get_next_for_answer_id(answer.answer_id)
    elif last_question.type == "multiple":
        if not isinstance(answer, MultipleChoiceResponse):
            raise_for_format()
        if len(answer.answers) >= 1:
            next_ = await get_next_for_answer_id(answer.answers[0])
        else:
            print("IN")
            next_ = await get_object(f"""
            MATCH (last_q) WHERE ID(last_q) = {last_question_id}
            MATCH (last_q)-[a_:ANSWER {{type:"empty"}}]->(q)
            """)
    elif last_question.type == "scale":
        if not isinstance(answer, ScaleResponse):
            raise_for_format()
        next_ = await get_object(f"""
        MATCH (last_q) WHERE ID(last_q) = {last_question_id}
        MATCH (last_q)-[_]->(q:Question) 
        """)
    else:
        raise DomainError(f"Invalid question type {last_question.type}")

    if next_.type != "finish":
        await redis.rpush(session_id, next_.id)
        await redis.expire(session_id, SESSION_TTL)
    else:
        await redis.delete(session_id)

    return next_
