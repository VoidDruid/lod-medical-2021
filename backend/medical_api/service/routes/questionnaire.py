# pylint: disable=C0413

import aioredis
from fastapi import Depends
from fastapi.responses import UJSONResponse
from pydantic import BaseModel

from dataplane import get_redis
from domain.questions import get_next_response
from domain.schemas import (
    AnswerModel,
    AnswerResponseModel,
)
from domain.session import create_session
from service.api import Api


api: Api = Api(tags=["Questions"])


class SessionResponse(BaseModel):
    session_id: str


@api.post("/init", response_model=SessionResponse)
async def session_start(redis: aioredis.Redis = Depends(get_redis)):
    return {
        "session_id": await create_session(redis),
    }


@api.post("/", response_model=AnswerResponseModel)
async def questions_endpoint(
    answer: AnswerModel, session_id: str, redis: aioredis.Redis = Depends(get_redis)
):
    return await get_next_response(redis, session_id, answer)
