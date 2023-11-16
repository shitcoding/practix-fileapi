import logging

from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from dependencies import get_redis, get_elasticsearch
from db.db import get_cache, get_storage
from db.base import Cache, Storage
from models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc: Film = await self.elastic.get(doc_id=film_id)
        except NotFoundError:
            return None
        return doc

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None
        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.id, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)


async def get_film_service(
    redis_client: Redis = Depends(get_redis),
    elastic_client: AsyncElasticsearch = Depends(get_elasticsearch),
) -> FilmService:
    redis: Cache = get_cache(model=Film, redis=redis_client)
    elastic: Storage = get_storage(model=Film, index="movies", elastic_client=elastic_client)
    return FilmService(redis=redis, elastic=elastic)

