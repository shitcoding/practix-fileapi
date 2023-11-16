from http import HTTPStatus

from core.config import DEFAULT_PAGE_SIZE
from fastapi import APIRouter, Depends, HTTPException
from models.genre import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get('/{uuid}', response_model=Genre)
async def genre_name(uuid: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(uuid)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return genre


@router.get('/', response_model=list[Genre])
async def genres_list(query: str = "", sort: str = "", page: int = 1, size: int = DEFAULT_PAGE_SIZE,
                      genre_service: GenreService = Depends(get_genre_service)) -> list[Genre]:
    genres = await genre_service.search(query=query, sort=sort, page=page, size=size)
    return genres
