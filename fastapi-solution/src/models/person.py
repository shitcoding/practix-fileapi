from enum import Enum

from models.templ_model import IdMix


class Role(Enum):
    ACTOR = 'actor'
    WRITER = 'writer'
    DIRECTOR = 'director'


class Person(IdMix):
    full_name: str


class FilmPerson(IdMix):
    roles: set[Role]


class PersonFilms(Person):
    films: list[FilmPerson]
