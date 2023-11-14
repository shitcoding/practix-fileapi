from models.templ_model import IdMix
from models.other_model import Genre,Person
from pydantic.typing import Literal


class FilmBase(IdMix):
    title: str
    imdb_rating: str | float | None

class Film(FilmBase):  
    description: str | None
    genres: list[Genre]
    directors: list[Person]
    actors: list[Person]
    writers: list[Person]

class FilmPerson(IdMix):
    roles  : Literal['actor','writer','director']