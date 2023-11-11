from templ_model import IdMix
from other_model import Genre,Person

class Filmwork(IdMix):
    rating: str | float | None
    title: str
    description: str | None
    type: str
    genres_names: list[str] = None
    genres: list[Genre]
    directors_names: list[str] = None
    directors: list[Person]
    actors_names: list[str] = None
    actors: list[Person]
    writers_names: list[str] = None
    writers: list[Person]
