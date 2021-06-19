import aioredis

from settings import redis_settings


class Redis:
    client: aioredis.Redis

    @classmethod
    async def create(cls):
        redis = await aioredis.from_url(redis_settings.uri)
        instance = cls()
        instance.client = redis
        return instance
