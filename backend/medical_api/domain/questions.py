import aioredis

from dataplane import neo4j

from .exceptions import DomainError
from .schemas import (
    AnswerModel,
    AnswerResponseModel,
    DoctorChoice,
    QuestionModel,
    ResultModel,
)


from .schemas import (  # isort: skip
    ScaleQuestion,
    MultipleChoiceQuestion,
    SingleChoiceQuestion,
    BodySchemaQuestion,
    ChoiceOption,
    ScaleSection,
)

mock_questions = [
    SingleChoiceQuestion(
        id=0,
        title="Первичное обращение?",
        answers=[ChoiceOption(id=1, text="Да"), ChoiceOption(id=1, text="Нет")],
    ),
    SingleChoiceQuestion(
        id=1,
        title="Оцените уровень боли?",
        type="scale",
        answers=[
            ChoiceOption(
                id="1,3",
                text="\bСлабая боль\b\nПочти не мешает заниматься обычными делами",
            ),
            ChoiceOption(
                id="4,6",
                text="\bУмеренная боль\b\nМешает обычной жизни и не дает забыть о себе",
            ),
            ChoiceOption(
                id="7,10",
                text="\bСильная боль\b\nЗатмевает всё, делает человека зависимым от помощи других",
            ),
        ],
    ),
    MultipleChoiceQuestion(
        id=2,
        title="Укажетие, есть ли у вас следующие симптомы",
        answers=[
            ChoiceOption(id=1, text="Боли в левой половине грудной клетки"),
            ChoiceOption(id=2, text="Продолжающееся кровотечение"),
            ChoiceOption(id=3, text="Нарушение дыханият"),
            ChoiceOption(
                id=4,
                text="Резкое головокружение или неустойчивость, не можете идти, вынуждены лечь",
            ),
            ChoiceOption(
                id=5,
                text="Тошнота, рвота, повышение температуры, связанные с употреблением конкретных продуктов",
            ),
        ],
    ),
    MultipleChoiceQuestion(
        id=3,
        title="Укажетие, есть ли у вас следующие симптомы",
        answers=[
            ChoiceOption(id=1, text="Нарушение обоняния, повышение температуры"),
            ChoiceOption(id=2, text="Жидкий стул больше пяти раз в день"),
            ChoiceOption(
                id=3, text="Температура выше 38 вместе с насморком или кашлем"
            ),
            ChoiceOption(
                id=4, text="Пожелтение кожи, глазных белков и повышенная температура"
            ),
        ],
    ),
    SingleChoiceQuestion(
        id=4,
        title="Первичное обращение?",
        answers=[ChoiceOption(id=1, text="Да"), ChoiceOption(id=1, text="Нет")],
    ),
    BodySchemaQuestion(
        id=5,
        title="Укажите что вас беспокоит",
    ),
    MultipleChoiceQuestion(
        id=6,
        title="Живот",
        answers=[
            ChoiceOption(id=1, text="Диарея"),
            ChoiceOption(id=2, text="Боли"),
        ],
    ),
]


def get_initial_question() -> QuestionModel:
    # TODO: actual logic
    return mock_questions[0]


async def get_next_response(
    redis: aioredis.Redis, session_id: str, answer: AnswerModel
) -> AnswerResponseModel:
    last_question_id = await redis.lrange(session_id, -1, -1)
    if last_question_id is None or len(last_question_id) == 0:
        raise DomainError(f"session_id {session_id} does not exist")

    last_question_id = int(last_question_id[0])

    if last_question_id != answer.question_id:
        raise DomainError(f"Last question id was not {answer.question_id}")

    # TODO: actual logic
    next_ = answer.question_id + 1
    if next_ == 7:
        await redis.delete(session_id)
        return ResultModel(
            title="Хирург",
            choices=[
                DoctorChoice(name="Айболит", clinic="Африка"),
            ],
        )

    await redis.rpush(session_id, next_)
    return mock_questions[next_]
