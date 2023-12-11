import json
import logging
from functools import lru_cache
from typing import List, Optional

from core.config import settings
from db.base import Cache, Storage
from db.db import get_cache, get_storage
from elasticsearch_dsl import Search
from fastapi import Depends
from models.genre import Genre
from services.base import ExtService

logger = logging.getLogger(__name__)


class GenreService(ExtService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_prefix = "GENRE"

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._get_genre_from_cache(genre_id)

        if not genre:
            genre = await self._get_genre_from_storage(genre_id)
            if not genre:
                raise Exception(f"Genre {genre_id} not found")
            await self._put_genre_to_cache(genre)

        return genre

    async def search(self, query: str, sort: str, page: int, size: int) -> list[Optional[Genre]]:
        search_query = self._build_search_query(query, sort, page, size)

        genres = await self._get_genres_from_cache(search_query.to_dict())

        if not genres:
            genres = await self._get_genres_from_storage(search_query)

            if not genres:
                raise Exception(f"Genres with query {query} not found")
            await self._put_genres_to_cache(search_query.to_dict(), genres)

        return genres

    async def _get_genre_from_storage(self, genre_id: str) -> Optional[Genre]:
        return await self.storage.get(doc_id=genre_id)

    async def _get_genres_from_storage(self, query: Search) -> List[Genre]:
        return await self.storage.search(query=query.to_dict())

    async def _get_genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        data = await self.cache.get(f"{self.cache_prefix}:{genre_id}")
        if not data:
            return None
        deserialized_data = json.loads(data)
        genre = Genre.parse_obj(deserialized_data)
        return genre

    async def _get_genres_from_cache(self, query: dict) -> List[Genre]:
        return await self.cache.get_list(f"{self.cache_prefix}:{json.dumps(query)}")

    async def _put_genre_to_cache(self, genre: Genre):
        await self.cache.set(f"{self.cache_prefix}:{genre.uuid}", genre, settings.redis.redis_expire)

    async def _put_genres_to_cache(self, query: dict, genres: list[Genre]):
        await self.cache.set_list(f"{self.cache_prefix}:{json.dumps(query)}", genres, settings.redis.redis_expire)

    @staticmethod
    def _build_search_query(query: str, sort: str, page: int, size: int):
        s = Search()
        if query:
            multi_match_fields = ('name',)

            s = s.query("multi_match", query=query, fields=multi_match_fields)
        if sort:
            s = s.sort(sort)
        start = (page - 1) * size
        return s[start: start + size]


@lru_cache()
def get_genre_service(
        cache: Cache = Depends(get_cache),
        storage: Storage = Depends(get_storage)

) -> GenreService:
    return GenreService(cache.init(model=Genre), storage.init(model=Genre, index=settings.elastic.es_genres_index))
