import orjson
from datetime import date
from typing import Optional
from enum import Enum

from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Role(Enum):
    actor = 'actor'
    writer = 'writer'
    director = 'director'


class PersonBase(BaseModel):
    id: str
    name: str


class PersonFilm(BaseModel):
    uuid: str
    roles: Optional[list[Role]] = []


class Person(PersonBase):
    films: Optional[list[PersonFilm]] = []


class Genre(BaseModel):
    id: str#-----------------------------------------
    name: str


class FilmBase(BaseModel):
    id: str
    title: str
    imdb_rating: float


class Film(FilmBase):
    description: str
    creation_date: date
    # genre: Optional[list[Genre]] = []
    actors: Optional[list[PersonBase]] = []
    writers: Optional[list[PersonBase]] = []
    # directors: Optional[list[PersonBase]] = []

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps

