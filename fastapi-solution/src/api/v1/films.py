from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from services.film import FilmService, get_film_service

from typing import Optional

from .api_models import Film, Genre, PersonBase, PageAnswer, FilmBase as FilmAnswer

from models.film import FilmBase

from core.config import PAGE_SIZE, SORT_FIELD

router = APIRouter()


@router.get('/search', response_model=PageAnswer)
async def query_films(query: str, page: int=1, size: int=PAGE_SIZE, film_service: FilmService=Depends(get_film_service)) -> PageAnswer:
    """
    Метод получает список фильмов по запросу
    """
    films: list[FilmBase] = await film_service.get_films_query(page, size, query)
    page_model = PageAnswer(
        page_size=size,
        number_page=page,
        amount_elements=len(films),
        result=[FilmAnswer.parse_obj(film_obj.dict()) for film_obj in films]
    )
    return page_model


@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return Film(
        uuid=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        creation_date=film.creation_date,
        actors=[PersonBase(full_name=i.name, uuid=i.id) for i in film.actors],
        writers=[PersonBase(full_name=i.name, uuid=i.id) for i in film.writers],
        directors=[PersonBase(full_name=i.name, uuid=i.id) for i in film.director],
        genre=[Genre(name=i.name, uuid=i.id) for i in film.genre],
    )

@router.get('/', response_model=PageAnswer)
async def all_films(page: int=1, size: int=PAGE_SIZE, sort: str = SORT_FIELD, genre: str=None,film_service: FilmService=Depends(get_film_service)) -> PageAnswer:
    # получаем список фильмов с определенного места определенного размера
    films: list[FilmBase] = await film_service.get_films_page(page, size, sort, genre)
    page_model = PageAnswer(
        page_size=size,
        number_page=page,
        amount_elements=len(films),
        result=[FilmAnswer.parse_obj(film_obj.dict()) for film_obj in films]
    )
    return page_model
