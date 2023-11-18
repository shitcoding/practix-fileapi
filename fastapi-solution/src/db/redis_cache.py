import json

from pydantic import BaseModel, TypeAdapter
from redis.asyncio import Redis

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

    async def set(self, key: str, value: BaseModel, expire: int):
        await self.client.set(key, value.model_dump_json(), expire)

    async def get_list(self, key: str) -> list[BaseModel]:
        data = await self.client.get(key)
        if not data:
            return []
        ta = TypeAdapter(list[self.model])
        return ta.validate_json(data)

    async def set_list(self, key: str, value: list[BaseModel], expire: int):
        ta = TypeAdapter(list[self.model])
        json_data = ta.dump_json(value)
        await self.client.set(key, json_data, expire)
