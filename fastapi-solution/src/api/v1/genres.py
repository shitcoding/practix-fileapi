import logging
from http import HTTPStatus

from core.config import DEFAULT_PAGE_SIZE
from fastapi import APIRouter, Depends, HTTPException
from models.genre import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get('/{uuid}', response_model=Genre)
async def genre_name(uuid: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    try:
        genre = await genre_service.get_by_id(uuid)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genre not found')
    return genre


@router.get('/', response_model=list[Genre])
async def genres_list(query: str = "", sort: str = "", page_number: int = 1, page_size: int = DEFAULT_PAGE_SIZE,
                      genre_service: GenreService = Depends(get_genre_service)) -> list[Genre]:
    try:
        genres = await genre_service.search(query=query, sort=sort, page=page_number, size=page_size)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genres not found')
    return genres
