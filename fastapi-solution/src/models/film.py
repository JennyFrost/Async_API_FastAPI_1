from datetime import date

from models.base_config import BaseOrjsonModel


class PersonBase(BaseOrjsonModel):
    id: str
    name: str


class Genre(BaseOrjsonModel):
    id: str
    name: str


class FilmBase(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: float | None


class Film(FilmBase):
    description: str | None
    creation_date: date | None = None
    genre: list[Genre] | None = []
    actors: list[PersonBase] | None = []
    writers: list[PersonBase] | None = []
    director: list[PersonBase] | None = []
