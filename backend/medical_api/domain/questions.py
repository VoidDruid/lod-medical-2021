from typing import Tuple

import aioredis
from neo4j import Transaction
from pydantic import parse_obj_as

from dataplane import neo4j

from .exceptions import DomainError
from .schemas import (
    AnswerModel,
    AnswerResponseModel,
    MultipleChoiceResponse,
    QuestionModel,
    ResultModel,
    ScaleResponse,
    SingleChoiceResponse,
)


async def get_entry_question() -> Tuple[int, QuestionModel]:
    def question_query(tx: Transaction):
        get_initial = """
        MATCH (q:Question {entry:true})
        MATCH (_)<-[answers:ANSWER]-(q)
        RETURN id(q), q, answers
        """
        return tx.run(get_initial).single()

    result = await neo4j(question_query)
    if len(result) == 0:
        raise DomainError("No entry question found")
    id_ = result["id(q)"]
    q = dict(result["q"])
    print(result["answers"])
    q.pop("entry")

    return parse_obj_as(QuestionModel, {
        "id": id_,
        **q
    })


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
