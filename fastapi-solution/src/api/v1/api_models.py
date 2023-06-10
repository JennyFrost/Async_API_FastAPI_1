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
    imdb_rating: Optional[float]

    @classmethod
    def parse_obj(cls, obj: dict):
        obj = {
            "uuid": obj.get("id"),
            "title": obj.get("title"),
            "imdb_rating": obj.get("imdb_rating")
        }
        return super().parse_obj(obj)


class PageAnswer(BaseModel):
    page_size: int
    number_page: int
    amount_elements: int 
    result: Optional[list[FilmBase]] = []


class Film(FilmBase):
    description: str
    creation_date: Optional[date] = None
    actors: Optional[list[PersonBase]] = []
    writers: Optional[list[PersonBase]] = []
    directors: Optional[list[PersonBase]] = []
    genre: Optional[list[Genre]] = []
