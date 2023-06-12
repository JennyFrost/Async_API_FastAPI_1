import orjson
from datetime import date

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
    imdb_rating: float | None

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Film(FilmBase):
    description: str | None
    creation_date: date | None = None
    genre: list[Genre] | None = []
    actors: list[PersonBase] | None = []
    writers: list[PersonBase] | None = []
    director: list[PersonBase] | None = []
