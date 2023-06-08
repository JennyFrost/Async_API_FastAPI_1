from pydantic import BaseModel
from typing import Optional
from datetime import date

from models.person import Role


class PersonFilm(BaseModel):
    uuid: str
    roles: Optional[list[Role]] = []


class PersonBase(BaseModel):
    uuid: str
    full_name: str


class Person(PersonBase):
    films: Optional[list[PersonFilm]] = []


class Genre(BaseModel):
    uuid: str
    name: str


class FilmBase(BaseModel):
    uuid: str
    title: str
    imdb_rating: float


class Film(FilmBase):
    description: str
    creation_date: Optional[date] = None
    actors: Optional[list[PersonBase]] = []
    writers: Optional[list[PersonBase]] = []
    directors: Optional[list[PersonBase]] = []
    genre: Optional[list[Genre]] = []


class FilmBase(BaseModel):
    uuid: str
    title: str
    imdb_rating: float
