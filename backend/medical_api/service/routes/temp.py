# pylint: disable=C0413

from typing import Any

from neo4j import Transaction

from dataplane import neo4j
from domain.schemas import (
    BodySchemaQuestion,
    MultipleChoiceQuestion,
    MultipleChoiceResponse,
    ScaleQuestion,
    ScaleResponse,
    SingleChoiceQuestion,
    SingleChoiceResponse,
)
from service.api import Api


api: Api = Api(tags=["ВРЕМЕННО"])


@api.post("/scale", response_model=ScaleQuestion, name="ДЕМОНСТРАЦИОННЫЙ РОУТ")
def variant_1(scale_response: ScaleResponse):
    pass


@api.post(
    "/single-choice", response_model=SingleChoiceQuestion, name="ДЕМОНСТРАЦИОННЫЙ РОУТ"
)
def variant_1(choice_response: SingleChoiceResponse):
    pass


@api.post(
    "/multiple-choice",
    response_model=MultipleChoiceQuestion,
    name="ДЕМОНСТРАЦИОННЫЙ РОУТ",
)
def variant_1(choices_response: MultipleChoiceResponse):
    pass


@api.post(
    "/body-schema",
    response_model=BodySchemaQuestion,
    name="ДЕМОНСТРАЦИОННЫЙ РОУТ",
)
def variant_1(choices_response: SingleChoiceResponse):
    pass


@api.post("/tests", response_model=Any)
async def variant_1() -> Any:
    def q(tx: Transaction):
        get_initial = "MATCH (q:Question {entry:true}) RETURN q"
        drop_all = "MATCH (n) DETACH DELETE n"
        result = tx.run(get_initial).single()
        return result

    return await neo4j(q)
