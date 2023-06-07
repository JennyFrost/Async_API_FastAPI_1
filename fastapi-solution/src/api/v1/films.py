from http import HTTPStatus
from typing import Optional
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.film import FilmService, get_film_service
from .genres import Genre
from .persons import PersonBase

router = APIRouter()


class Film(BaseModel):
    uuid: str
    title: str
    imdb_rating: float
    description: str
    creation_date: Optional[date] = None
    actors: Optional[list[PersonBase]] = []
    writers: Optional[list[PersonBase]] = []
    directors: Optional[list[PersonBase]] = []
    genre: Optional[list[Genre]] = []


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