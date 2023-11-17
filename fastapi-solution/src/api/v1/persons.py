from http import HTTPStatus

from core.config import DEFAULT_PAGE_SIZE
from fastapi import APIRouter, Depends, HTTPException
from models.film import FilmBase
from models.person import PersonFilms
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/{uuid}', response_model=PersonFilms)
async def person_name(uuid: str, person_service: PersonService = Depends(get_person_service)) -> PersonFilms:
    person = await person_service.get_by_id(uuid)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person


@router.get('/search/', response_model=list[PersonFilms])
async def persons_list(query: str = "", sort: str = "", page: int = 1, size: int = DEFAULT_PAGE_SIZE,
                       person_service: PersonService = Depends(get_person_service)) -> list[PersonFilms]:
    persons = await person_service.search(query=query, sort=sort, page=page, size=size)
    return persons


@router.get('/{uuid}/films', response_model=list[FilmBase])
async def person_films(uuid: str, sort: str = "", page: int = 1, size: int = DEFAULT_PAGE_SIZE,
                       person_service: PersonService = Depends(get_person_service)) -> list[FilmBase]:
    films = await person_service.film_search(uuid=uuid, sort=sort, page=page, size=size)
    return films
