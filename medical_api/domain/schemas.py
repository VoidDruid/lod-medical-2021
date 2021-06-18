from typing import List

from pydantic import BaseModel


class ChoiceOption(BaseModel):
    id: int
    text: str


class ScaleItem(BaseModel):
    min: int
    max: int
    description: str


class Question(BaseModel):
    title: str
    text: str


class ScaleQuestion(Question):
    min: int
    max: int
    step: int = 1
    items: List[ScaleItem]


class ChoiceQuestion(Question):
    type: str
    answers: List[ChoiceOption]


class SingleChoiceQuestion(ChoiceQuestion):
    type = "single"


class MultipleChoiceQuestion(ChoiceQuestion):
    type = "multiple"
    max_choices: int = 0


# --- Responses ---


class QuestionResponse(BaseModel):
    question_id: int


class SingleChoiceResponse(QuestionResponse):
    answer_id: int


class MultipleChoiceResponse(QuestionResponse):
    answers: List[int]


class ScaleResponse(QuestionResponse):
    value: int
