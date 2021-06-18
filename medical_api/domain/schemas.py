from typing import List

from pydantic import BaseModel


class ScaleItem(BaseModel):
    min: int
    max: int
    description: str


class ScaleQuestion(BaseModel):
    min: int
    max: int
    step: int = 1
    items: List[ScaleItem]


class ChoiceOption(BaseModel):
    id: int
    text: str


class ChoiceQuestion(BaseModel):
    title: str
    text: str
    type: str
    answers: List[ChoiceOption]


class SingleChoiceQuestion(ChoiceQuestion):
    type = "single"


class MultipleChoiceQuestion(ChoiceQuestion):
    type = "multiple"
    max_choices: int = 0
