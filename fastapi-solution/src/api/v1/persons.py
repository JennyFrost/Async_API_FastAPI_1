from http import HTTPStatus
from typing import Optional
from enum import Enum

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.person import PersonService, get_person_service
from models.person import Role

router = APIRouter()



class PersonFilm(BaseModel):
    uuid: str
    roles: Optional[list[Role]] = []


class PersonBase(BaseModel):
    uuid: str
    full_name: str


class Person(PersonBase):
    films: Optional[list[PersonFilm]] = []


@router.get('/{person_id}', response_model=Person)
async def film_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    return Person(uuid=person.uuid, full_name=person.full_name, films=person.films)
