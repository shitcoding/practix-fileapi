from pydantic import Field, validator

from typing import Optional, Union
from models.templ_model import IdMix
from models.genre import Genre
from models.person import Person


class Film(IdMix):
    imdb_rating: Optional[Union[str, float]]
    title: Optional[str]
    description: Optional[str]
    file_path: Optional[str]
    genre: list[Genre]
    directors: Optional[list[Person]]
    actors: Optional[list[Person]]
    writers: Optional[list[Person]]

    @validator('directors', pre=True)
    def convert_director_to_list(cls, v):
        return v if isinstance(v, list) else None


class FilmList(IdMix):
    title: str
    imdb_rating: float = Field(None)
    genre: list[Genre]

    class Config:
        allow_population_by_field_name = True


class FilmSearchResult(IdMix):
    title: str
    imdb_rating: float
