import orjson
from datetime import date
from typing import Optional

from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class PersonBase(BaseModel):
    id: str
    name: str


class Genre(BaseModel):
    id: str
    name: str


class FilmBase(BaseModel):
    id: str
    title: str
    imdb_rating: Optional[float]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Film(FilmBase):
    description: Optional[str]
    creation_date: Optional[date] = None
    genre: Optional[list[Genre]] = []
    actors: Optional[list[PersonBase]] = []
    writers: Optional[list[PersonBase]] = []
    director: Optional[list[PersonBase]] = []
