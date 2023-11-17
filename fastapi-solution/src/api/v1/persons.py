import logging
from http import HTTPStatus

from core.config import DEFAULT_PAGE_SIZE
from fastapi import APIRouter, Depends, HTTPException
from models.film import FilmBase
from models.person import PersonFilms
from services.person import PersonService, get_person_service

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get('/{uuid}', response_model=PersonFilms)
async def person_name(uuid: str, person_service: PersonService = Depends(get_person_service)) -> PersonFilms:
    try:
        person = await person_service.get_by_id(uuid)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Person not found')
    return person


@router.get('/search/', response_model=list[PersonFilms])
async def persons_list(query: str = "", sort: str = "", page: int = 1, size: int = DEFAULT_PAGE_SIZE,
                       person_service: PersonService = Depends(get_person_service)) -> list[PersonFilms]:
    try:
        persons = await person_service.search(query=query, sort=sort, page=page, size=size)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Persons not found')
    return persons


@router.get('/{uuid}/films', response_model=list[FilmBase])
async def person_films(uuid: str, sort: str = "", page: int = 1, size: int = DEFAULT_PAGE_SIZE,
                       person_service: PersonService = Depends(get_person_service)) -> list[FilmBase]:
    try:
        films = await person_service.film_search(uuid=uuid, sort=sort, page=page, size=size)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Films not found')
    return films
