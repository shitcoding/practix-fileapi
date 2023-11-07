from dataclasses import astuple, dataclass, field
from enum import Enum
from typing import Dict, List
from uuid import UUID


class Role(Enum):
    ACTOR = 'actor'
    WRITER = 'writer'
    DIRECTOR = 'director'

    def __str__(self):
        return self.value


@dataclass
class Data:
    def to_str_tuple(self):
        func = (lambda obj: obj if obj is None else str(obj))
        return tuple(map(func, astuple(self)))


@dataclass
class Person(Data):
    id:         UUID
    name:       str
    role:       Role


@dataclass
class Genre(Data):
    id:          UUID
    name:        str


@dataclass
class FilmWork(Data):
    id:             UUID
    title:          str
    description:    str
    rating:         float
    genres:         Dict[str, Genre] = field(default_factory=dict)
    persons:        Dict[str, Person] = field(default_factory=dict)


@dataclass
class ESPerson:
    id: str
    name: str


@dataclass
class ESData:
    id:             str
    imdb_rating:    float
    genre:          list[str]
    title:          str
    description:    str
    director:       str
    actors_names:   list[str]
    writers_names:  list[str]
    actors:         List[ESPerson]
    writers:        List[ESPerson]



