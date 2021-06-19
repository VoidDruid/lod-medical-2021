# pylint: disable=C0413

from typing import List, Any

from fastapi import Depends
from neo4j import Transaction
from sqlalchemy.orm import Session

import crud
from service.api import Api
from service.dependencies import get_redis
from dataplane import neo4j

from domain.schemas import (
    ScaleQuestion,
    SingleChoiceQuestion,
    MultipleChoiceQuestion,
    SingleChoiceResponse,
    MultipleChoiceResponse,
    ScaleResponse,
)

api: Api = Api(tags=["ВРЕМЕННО"])


@api.post("/scale", response_model=ScaleQuestion, name="ДЕМОНСТРАЦИОННЫЙ РОУТ")
def variant_1(scale_response: ScaleResponse):
    pass


@api.post("/single-choice", response_model=SingleChoiceQuestion, name="ДЕМОНСТРАЦИОННЫЙ РОУТ")
def variant_1(choice_response: SingleChoiceResponse):
    pass


@api.post("/multiple-choice", response_model=MultipleChoiceQuestion, name="ДЕМОНСТРАЦИОННЫЙ РОУТ")
def variant_1(choices_response: MultipleChoiceResponse):
    pass


@api.post("/tests", response_model=Any)
async def variant_1() -> Any:
    def q(tx: Transaction):
        create_all = """
        CREATE (TheMatrix:Movie {title:'The Matrix', released:1999, tagline:'Welcome to the Real World'})
        CREATE (Keanu:Person {name:'Keanu Reeves', born:1964})
        CREATE (Carrie:Person {name:'Carrie-Anne Moss', born:1967})
        CREATE (Laurence:Person {name:'Laurence Fishburne', born:1961})
        CREATE (Hugo:Person {name:'Hugo Weaving', born:1960})
        CREATE (LillyW:Person {name:'Lilly Wachowski', born:1967})
        CREATE (LanaW:Person {name:'Lana Wachowski', born:1965})
        CREATE (JoelS:Person {name:'Joel Silver', born:1952})
        CREATE 
        (Keanu)-[:ACTED_IN {roles:['Neo']}]->(TheMatrix),
        (Carrie)-[:ACTED_IN {roles:['Trinity']}]->(TheMatrix),
        (Laurence)-[:ACTED_IN {roles:['Morpheus']}]->(TheMatrix),
        (Hugo)-[:ACTED_IN {roles:['Agent Smith']}]->(TheMatrix),
        (LillyW)-[:DIRECTED]->(TheMatrix),
        (LanaW)-[:DIRECTED]->(TheMatrix),
        (JoelS)-[:PRODUCED]->(TheMatrix)
        RETURN Keanu,Carrie,Laurence,Hugo,LillyW,LanaW,JoelS
        """
        drop_all = "MATCH (n) DETACH DELETE n"
        result = tx.run(create_all).single()
        return result
    return await neo4j(q)
