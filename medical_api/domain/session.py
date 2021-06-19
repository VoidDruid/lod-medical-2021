from typing import Tuple
from uuid import uuid4

import aioredis

from .questions import get_initial_question
from .schemas import Question


def create_session_id() -> str:
    return uuid4().hex


async def create_session(redis: aioredis.Redis) -> Tuple[str, Question]:
    session_id = create_session_id()

    initial_question = get_initial_question()

    await redis.rpush(session_id, initial_question.id)

    return session_id, initial_question
