from models.templ_model import IdMix
from models.other_model import Genre,Person

class Film(IdMix):
    imdb_rating: str | float | None
    title: str
    description: str | None
    genres: list[Genre]
    directors: list[Person]
    actors: list[Person]
    writers: list[Person]
