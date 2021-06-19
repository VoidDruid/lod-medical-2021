from typing import Tuple
from uuid import uuid4

import aioredis

from .questions import get_initial_question
from .schemas import Question


SESSION_TTL = 60 * 10


def create_session_id() -> str:
    return uuid4().hex


async def create_session(redis: aioredis.Redis) -> Tuple[str, Question]:
    session_id = create_session_id()

    initial_question = get_initial_question()

    await redis.rpush(session_id, initial_question.id)
    await redis.expire(session_id, SESSION_TTL)

    return session_id, initial_question
