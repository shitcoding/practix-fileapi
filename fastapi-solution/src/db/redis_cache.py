import json

from redis.asyncio import Redis

from pydantic import BaseModel, TypeAdapter
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

    async def get_list(self, key: str) -> list[BaseModel]:
        data = await self.client.get(key)
        if not data:
            return []
        ta = TypeAdapter(list[self.model])
        return ta.validate_json(data)

    async def set_list(self, key: str, value: list, expire: int):
        json_data = json.dumps([item.json() for item in value])
        await self.client.set(key, json_data, expire)
