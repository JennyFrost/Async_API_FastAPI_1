import orjson
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
    uuid: str
    full_name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class PersonFilm(BaseModel):
    uuid: str
    roles: Optional[list[Role]] = []


class Person(PersonBase):
    films: Optional[list[PersonFilm]] = []