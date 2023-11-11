from dataclasses import astuple, dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class Role(Enum):
    ACTOR = 'actor'
    WRITER = 'writer'
    DIRECTOR = 'director'

    def __str__(self):
        return self.value


class FilmWorkType(Enum):
    MOVIE = 'movie'
    TV_SHOW = 'tv_show'

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
    full_name:  str
    created:    datetime
    modified:   datetime


@dataclass
class Genre(Data):
    id:          UUID
    name:        str
    description: str
    created:     datetime
    modified:    datetime


@dataclass
class FilmWork(Data):
    id:             UUID
    title:          str
    description:    str
    creation_date:  datetime
    file_path:      str
    rating:         float
    type:           FilmWorkType
    created:        datetime
    modified:       datetime


@dataclass
class PersonFilmWork(Data):
    id:            UUID
    film_work_id:  UUID
    person_id:     UUID
    role:          Role
    created:       datetime


@dataclass
class GenreFilmWork(Data):
    id:            UUID
    film_work_id:  UUID
    genre_id:      UUID
    created:       datetime


tables = {
    'person': Person,
    'genre': Genre,
    'film_work': FilmWork,
    'person_film_work': PersonFilmWork,
    'genre_film_work': GenreFilmWork
}
