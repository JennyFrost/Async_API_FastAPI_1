from http import HTTPStatus
from typing import Optional
from enum import Enum

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.person import PersonService, get_person_service
from .genres import Genre

router = APIRouter()


class Role(Enum):
    actor = 'actor'
    writer = 'writer'
    director = 'director'


class PersonFilm(BaseModel):
    uuid: str
    roles: Optional[list[Role]] = []


class PersonBase(BaseModel):
    uuid: str
    full_name: str


class Person(PersonBase):
    films: Optional[list[PersonFilm]] = []


@router.get('/{person_id}', response_model=PersonBase)
async def film_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> PersonBase:
    person = await person_service.get_by_id(person_id)
    return PersonBase(uuid=person.uuid, full_name=person.full_name)