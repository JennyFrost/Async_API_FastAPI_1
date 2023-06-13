from enum import Enum

from models.base_config import BaseOrjsonModel

class Role(Enum):
    actor = 'actor'
    writer = 'writer'
    director = 'director'


class PersonBase(BaseOrjsonModel):
    uuid: str
    full_name: str


class PersonFilm(BaseOrjsonModel):
    uuid: str
    roles: list[Role] = []


class Person(PersonBase):
    films: list[PersonFilm] = []
