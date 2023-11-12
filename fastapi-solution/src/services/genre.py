from typing import Optional
from functools import lru_cache
from fastapi import Depends

from services.base import Service
from db.db import get_cache, get_storage
from db.base import Cache, Storage
from models.film import Genre
from core.config import EXPIRE


class GenreService(Service):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_prefix = "GENRE"

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._get_genre_from_cache(genre_id)
        if not genre:
            genre = await self.storage.get(id=genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)

        return genre

    async def _get_genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        return await self.cache.get(f"{self.cache_prefix}:{genre_id}")

    async def _put_genre_to_cache(self, genre: Genre):
        await self.cache.set(f"{self.cache_prefix}:{genre.id}", genre, EXPIRE)


@lru_cache()
def get_genre_service(
        cache: Cache = Depends(get_cache(model=Genre)),
        storage: Storage = Depends(get_storage(model=Genre, index="genres")),
) -> GenreService:
    return GenreService(cache, storage)
