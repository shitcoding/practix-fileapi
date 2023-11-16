from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.models.film import FilmList, FilmSearchResult

from app.models.film import Film
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get("/", response_model=list[FilmList])
async def list_films(
        sort: Optional[str] = Query(None),
        genre: Optional[str] = None,
        film_service: FilmService = Depends(get_film_service)
):
    films = await film_service.list_films(genre=genre, sort=sort)
    return films


@router.get("/search", response_model=list[FilmSearchResult])
async def search_films(
        query: str = Query(None),
        page_number: int = Query(1),
        page_size: int = Query(50),
        film_service: FilmService = Depends(get_film_service)
):
    return await film_service.search_films(
        query=query,
        page_number=page_number,
        page_size=page_size,
    )


@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return Film(id=film.id, title=film.title)
