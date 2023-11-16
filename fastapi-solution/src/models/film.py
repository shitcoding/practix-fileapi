from models.genre import Genre
from models.person import Person
from models.templ_model import IdMix


class FilmBase(IdMix):
    title: str
    imdb_rating: str | float | None


class Film(FilmBase):  
    description: str | None
    genre:  list[Genre]
    directors: list[Person]
    actors: list[Person]
    writers: list[Person]

