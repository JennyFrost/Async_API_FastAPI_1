from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from services.film import FilmService, get_film_service

from .api_models import Film, Genre, PersonBase, FilmBase as FilmAnswer

from models.film import FilmBase

router = APIRouter()


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

# @router.get('/', response_model=list[FilmAnswer])
# async def all_films(size: int=40, func: some_func = ) -> list[FilmAnswer]:

