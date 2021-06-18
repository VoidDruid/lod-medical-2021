# pylint: disable=C0413

from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

import crud
from database import *
from service.api import Api
from service.dependencies import get_db

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
def variant_1(choices_reponse: MultipleChoiceResponse):
    pass
