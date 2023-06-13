from pydantic import BaseModel
from datetime import date

from models.person import Role


class PersonFilm(BaseModel):
    uuid: str
    roles: list[Role] | None = []


class PersonBase(BaseModel):
    uuid: str
    full_name: str


class Person(PersonBase):
    films: list[PersonFilm] | None = []


class Genre(BaseModel):
    uuid: str
    name: str


class FilmBase(BaseModel):
    uuid: str
    title: str
    imdb_rating: float | None

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
    result: list[FilmBase] | None = []


class Film(FilmBase):
    description: str | None
    creation_date: date | None = None
    actors: list[PersonBase] | None = []
    writers: list[PersonBase] | None = []
    directors: list[PersonBase] | None = []
    genre: list[Genre] | None = []
