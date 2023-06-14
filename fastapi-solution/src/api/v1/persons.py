from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from services.person import PersonService, get_person_service
from services.film import FilmService, get_film_service
from .api_models import Person, FilmBase
from core.config import settings

PAGE_SIZE = settings.page_size
SORT_FIELD = settings.sort_field

router = APIRouter()


@router.get('/search', response_model=list[Person])
async def search_person(
        query: str,
        page_number: Annotated[int, Query(description='Pagination page number', ge=1)] = 1,
        page_size: Annotated[int, Query(description='Pagination page size', ge=1)] = PAGE_SIZE,
        person_service: PersonService = Depends(get_person_service)) -> list[Person]:
    """
    Метод возвращает список людей (актеров/режисеров/сценаристов), которые соответствуют запросу поиска 
    
     - **query**: параметр поиска, поиск производится по полному имени человка
    """
    persons = await person_service.search_person(query, page_number, page_size)
    return [Person(uuid=person.uuid, full_name=person.full_name, films=person.films) for person in persons]


@router.get('/{person_id}', response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    """
    Метод возвращает информацию о человеке
    
     - **person_id**: id человека, по которому будет производиться поиск
    """
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return Person(uuid=person.uuid, full_name=person.full_name, films=person.films)


@router.get('/{person_id}/films', response_model=list[FilmBase])
async def person_films(
        person_id: str,
        page_number: Annotated[int, Query(description='Pagination page number', ge=1)] = 1,
        page_size: Annotated[int, Query(description='Pagination page size', ge=1)] = PAGE_SIZE,
        sort: str = SORT_FIELD,
        film_service: FilmService = Depends(get_film_service)) -> list[FilmBase]:
    """
    Метод возвращает список фильмов, в производстве которых участвовал человек

     - **person_id**: id человека, по которому будет производиться поиск
     - **sort**: параметр сортировки, по умолчанию сортировка идет по полю **rating** по убыванию
    """
    person_films = await film_service.get_person_films(person_id, page_size, page_number, sort)
    return [FilmBase(
        uuid=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating
    ) for film in person_films]