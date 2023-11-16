from redis.asyncio import Redis

from pydantic import BaseModel
from .base import Cache

class RedisCache(Cache):
    def __init__(self, model, redis: Redis):
        self.client = redis
        self.model = model

    async def get(self, key: str) -> BaseModel | None:
        data = await self.client.get(key)
        if not data:
            return None
        return data

    async def set(self, key: str, value: str, expire: int):
        await self.client.set(key, value, expire)

