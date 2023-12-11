import json
import logging
from functools import lru_cache
from typing import List, Optional
from copy import deepcopy

from core.config import settings
from db.base import Cache, Storage
from db.db import get_cache, get_storage
from elasticsearch_dsl import Q, Search
from fastapi import Depends
from models.film import Film, FilmSearchResult
from models.person import FilmPerson, Person, PersonFilms, Role
from services.base import ExtService

logger = logging.getLogger(__name__)


class PersonService(ExtService):
    def __init__(self, film_storage: Storage, film_cache: Cache, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_prefix = "PERSON"
        self.film_storage = film_storage
        self.film_cache = film_cache

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

    async def film_search(self, uuid: str, sort: str, page: int, size: int) -> list[FilmSearchResult]:
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
        print(persons)
        res = []
        for person in persons:
            short_films = await self._get_person_films(person["uuid"])
            res.append(PersonFilms(films=short_films, **person))
        return res

    async def _get_person_films_from_storage(self, person_id: str, sort: str, page: int, size: int)\
            -> List[FilmSearchResult]:
        film_search = self._build_film_search_query(person_id, sort, page, size)
        print(film_search.to_dict())
        films = await self.film_storage.search(query=film_search.to_dict())
        short_films = [FilmSearchResult(**film) for film in films]
        return short_films

    async def _get_person_from_cache(self, person_id: str) -> Optional[PersonFilms]:
        data = await self.cache.get(f"{self.cache_prefix}:{person_id}")
        if not data:
            return None
        deserialized_data = json.loads(data)
        person = PersonFilms.parse_obj(deserialized_data)
        return person

    async def _get_persons_from_cache(self, query: dict) -> List[PersonFilms]:
        return await self.cache.get_list(f"{self.cache_prefix}:{json.dumps(query)}")

    async def _put_person_to_cache(self, person: PersonFilms):
        await self.cache.set(f"{self.cache_prefix}:{person.uuid}", person, settings.redis.redis_expire)

    async def _put_persons_to_cache(self, query: dict, persons: list[PersonFilms]):
        await self.cache.set_list(f"{self.cache_prefix}:{json.dumps(query)}", persons, settings.redis.redis_expire)

    async def _get_person_films_from_cache(self, person_id: str) -> Optional[List[FilmSearchResult]]:
        return await self.film_cache.get_list(f"{self.cache_prefix}:{person_id}:films")

    async def _put_person_films_to_cache(self, person_id: str, films: list[FilmSearchResult]):
        await self.film_cache.set_list(f"{self.cache_prefix}:{person_id}:films", films, settings.redis.redis_expire)

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
            film = Film(**film)
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
        cache: Cache = Depends(get_cache),
        storage: Storage = Depends(get_storage)
) -> PersonService:

    person_cache = cache
    film_cache = deepcopy(cache)

    person_storage = storage
    film_storage = deepcopy(storage)

    return PersonService(cache=person_cache.init(model=PersonFilms),
                         storage=person_storage.init(model=Person, index=settings.elastic.es_persons_index),
                         film_storage=film_storage.init(model=Film, index=settings.elastic.es_movies_index),
                         film_cache=film_cache.init(model=FilmSearchResult))
