import json
import logging
from functools import lru_cache
from typing import List, Optional

from core.config import EXPIRE
from db.base import Cache, Storage
from db.db import get_cache, get_storage
from dependencies import get_elasticsearch, get_redis
from elasticsearch import AsyncElasticsearch
from elasticsearch_dsl import Q, Search
from fastapi import Depends
from models.film import Film, FilmBase
from models.person import FilmPerson, Person, PersonFilms, Role
from redis.asyncio import Redis
from services.base import Service

logger = logging.getLogger(__name__)


class PersonService(Service):
    def __init__(self, film_storage: Storage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_prefix = "PERSON"
        self.film_storage = film_storage

    async def get_by_id(self, person_id: str) -> Optional[PersonFilms]:
        person = await self._get_person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_storage(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)

        return person

    async def search(self, query: str, sort: str, page: int, size: int) -> list[Optional[PersonFilms]]:
        search_query = self._build_search_query(query, sort, page, size)

        persons = await self._get_persons_from_cache(search_query.to_dict())

        if not persons:
            persons = await self._get_persons_from_storage(search_query)

            if not persons:
                return []
            await self._put_persons_to_cache(search_query.to_dict(), persons)

        return persons

    async def film_search(self, uuid: str, sort: str, page: int, size: int) -> list[FilmBase]:
        films = await self._get_person_films_from_cache(uuid)
        if not films:
            films = await self._get_person_films_from_storage(person_id=uuid, sort=sort, page=page, size=size)
            if not films:
                return []
            await self._put_person_films_to_cache(uuid, films)
        return films

    async def _get_person_from_storage(self, person_id: str) -> Optional[PersonFilms]:
        person = await self.storage.get(doc_id=person_id)
        short_films = await self._get_person_films(person_id)
        return PersonFilms(uuid=person.uuid, full_name=person.full_name, films=short_films)

    async def _get_persons_from_storage(self, query: Search) -> List[PersonFilms]:
        persons = await self.storage.search(query=query.to_dict())
        res = []
        for person in persons:
            short_films = await self._get_person_films(person.uuid)
            res.append(PersonFilms(uuid=person.uuid, full_name=person.full_name, films=short_films))
        return res

    async def _get_person_films_from_storage(self, person_id: str, sort: str, page: int, size: int) -> List[FilmBase]:
        film_search = self._build_film_search_query(person_id, sort, page, size)
        films = await self.film_storage.search(query=film_search.to_dict())
        short_films = [FilmBase(uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating) for film in films]
        return short_films

    async def _get_person_from_cache(self, person_id: str) -> Optional[PersonFilms]:
        return await self.cache.get(f"{self.cache_prefix}:{person_id}")

    async def _get_persons_from_cache(self, query: dict) -> List[PersonFilms]:
        return await self.cache.get_list(f"{self.cache_prefix}:{json.dumps(query)}")

    async def _put_person_to_cache(self, person: PersonFilms):
        await self.cache.set(f"{self.cache_prefix}:{person.uuid}", person, EXPIRE)

    async def _put_persons_to_cache(self, query: dict, persons: list[PersonFilms]):
        await self.cache.set_list(f"{self.cache_prefix}:{json.dumps(query)}", persons, EXPIRE)

    async def _get_person_films_from_cache(self, person_id: str) -> Optional[List[FilmBase]]:
        return await self.cache.get_list(f"{self.cache_prefix}:{person_id}:films")

    async def _put_person_films_to_cache(self, person_id: str, films: list[FilmBase]):
        await self.cache.set_list(f"{self.cache_prefix}:{person_id}:films", films, EXPIRE)

    @staticmethod
    def _build_search_query(query: str, sort: str, page: int, size: int) -> Search:
        s = Search()
        if query:
            multi_match_fields = ('full_name',)

            s = s.query("multi_match", query=query, fields=multi_match_fields)
        if sort:
            s = s.sort(sort)
        start = (page - 1) * size
        return s[start: start + size]

    @staticmethod
    def _build_film_search_query(person_id: str, sort: str = None, page: int = None, size: int = None) -> Search:
        q_act_uuid = Q("nested", path="actors", query=Q("match", actors__uuid=person_id))
        q_wr_uuid = Q("nested", path="writers", query=Q("match", writers__uuid=person_id))
        q_dir_uuid = Q("nested", path="directors", query=Q("match", directors__uuid=person_id))
        s = Search().query(Q("bool", must=[q_act_uuid | q_wr_uuid | q_dir_uuid]))
        if sort:
            s = s.sort(sort)
        if page and size:
            start = (page - 1) * size
            s = s[start: start + size]
        return s

    async def _get_person_films(self, person_id: str) -> list[FilmPerson]:

        film_search = self._build_film_search_query(person_id)
        films = await self.film_storage.search(query=film_search.to_dict())
        short_films = []
        roles = set()
        for film in films:
            for actor in film.actors:
                if actor.uuid == person_id:
                    roles.add(Role.ACTOR)
                    break
            for writer in film.writers:
                if writer.uuid == person_id:
                    roles.add(Role.WRITER)
                    break
            for director in film.directors:
                if director.uuid == person_id:
                    roles.add(Role.DIRECTOR)
                    break
            short_films.append(FilmPerson(uuid=film.uuid, roles=roles))
        return short_films


@lru_cache()
def get_person_service(
        redis_client: Redis = Depends(get_redis),
        elastic_client: AsyncElasticsearch = Depends(get_elasticsearch)

) -> PersonService:
    cache: Cache = get_cache(model=PersonFilms, redis=redis_client)
    storage: Storage = get_storage(model=Person, index="persons", elastic=elastic_client)
    film_storage: Storage = get_storage(model=Film, index='movies', elastic=elastic_client)
    return PersonService(cache=cache, storage=storage, film_storage=film_storage)
