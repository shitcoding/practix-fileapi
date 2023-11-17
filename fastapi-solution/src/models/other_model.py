from typing import Optional
from pydantic import Field
from models.templ_model import IdMix


class Genre(IdMix):
    name: Optional[str]


class Person(IdMix):
    full_name: Optional[str] = Field(None, alias='name')