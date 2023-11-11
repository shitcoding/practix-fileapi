from typing import Optional
from redis.asyncio import Redis

from models.film import BaseModel
from .base import Cache


redis: Optional[Redis] = None


class RedisCache(Cache):
    def __init__(self, model):
        self.client = redis
        self.model = model

    async def get(self, key: str) -> BaseModel | None:
        return None

    async def set(self, key: str, value: BaseModel, expire: int):
        pass