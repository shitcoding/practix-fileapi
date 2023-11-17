from pydantic import BaseModel, UUID4, Field, validator

from typing import Optional, Union
from models.templ_model import IdMix
from models.other_model import Genre, Person


class Film(IdMix):
    imdb_rating: Optional[Union[str, float]]
    title: Optional[str]
    description: Optional[str]
    genre: list[str]
    director: Optional[list[Person]]
    actors: Optional[list[Person]]
    writers: Optional[list[Person]]

    @validator('director', pre=True)
    def convert_director_to_list(cls, v):
        return v if isinstance(v, list) else None


class FilmList(BaseModel):
    id: UUID4
    title: str
    imdb_rating: float = Field(None)
    genre: list[str]

    class Config:
        allow_population_by_field_name = True


class FilmSearchResult(BaseModel):
    id: UUID4
    title: str
    imdb_rating: float