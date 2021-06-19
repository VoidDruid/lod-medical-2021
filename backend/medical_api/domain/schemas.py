from typing import List, Optional, Union

from pydantic import BaseModel


class ChoiceOption(BaseModel):
    id: str
    text: str


class ScaleSection(BaseModel):
    min: int
    max: int
    description: str


# --- Questions ---


class BaseResponse(BaseModel):
    title: str


class Question(BaseResponse):
    type: str
    id: int
    text: str = ""


class BodySchemaQuestion(Question):
    type = "body"


class ScaleQuestion(Question):
    type = "scale"
    min: int
    max: int
    step: int = 1
    sections: List[ScaleSection]


class ChoiceQuestion(Question):
    answers: List[ChoiceOption]


class SingleChoiceQuestion(ChoiceQuestion):
    type = "single"


class MultipleChoiceQuestion(ChoiceQuestion):
    type = "multiple"


class DoctorChoice(BaseModel):
    name: str
    clinic: str
    avatar: str = ""


class ResultModel(BaseResponse):
    choices: Optional[List[DoctorChoice]]


QUESTION_MODELS = (
    ScaleQuestion,
    SingleChoiceQuestion,
    MultipleChoiceQuestion,
    BodySchemaQuestion,
)
QuestionModel = Union[QUESTION_MODELS]
AnswerResponseModel = Union[(*QUESTION_MODELS, ResultModel)]


# --- Responses ---


class QuestionResponse(BaseModel):
    question_id: int


class SingleChoiceResponse(QuestionResponse):
    answer_id: int


class MultipleChoiceResponse(QuestionResponse):
    answers: List[int]


class ScaleResponse(QuestionResponse):
    value: int


AnswerModel = Union[ScaleResponse, SingleChoiceResponse, MultipleChoiceResponse, QuestionResponse]
