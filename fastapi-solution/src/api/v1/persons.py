from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from services.person import PersonService, get_person_service
from services.film import FilmService, get_film_service
from .api_models import Person, FilmBase

router = APIRouter()


@router.get('/{person_id}', response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    """получить персонажа по id"""
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return Person(uuid=person.uuid, full_name=person.full_name, films=person.films)
