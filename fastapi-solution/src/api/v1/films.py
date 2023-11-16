from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.models.film import FilmList

from app.models.film import Film
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get("/all_movies", response_model=list[FilmList])
async def list_films(
    genre: Optional[str] = None,
    sort: Optional[str] = None,
    film_service: FilmService = Depends(get_film_service)
):
    films = await film_service.list_films(genre=genre, sort=sort)
    return films


@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return Film(id=film.id, title=film.title)
