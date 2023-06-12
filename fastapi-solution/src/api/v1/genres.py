from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from services.genre import GenreService, get_genres_service
from .api_models import Genre
from core.config import settings

PAGE_SIZE = settings.page_size

router = APIRouter()


@router.get('/', response_model=list[Genre])
async def list_genre(page_number: Annotated[int, Query(description='Pagination page number', ge=1, default=1)],
                     page_size: Annotated[int, Query(description='Pagination page size', ge=1, default=PAGE_SIZE)],
                     genre_service: GenreService = Depends(get_genres_service)) -> list[Genre]:
    genres = await genre_service.get_genres_list(page_number, page_size)
    return [Genre(uuid=genre.uuid, name=genre.name) for genre in genres]


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str,
                        genre_service: GenreService = Depends(get_genres_service)) -> Genre:
    """получить персонажа по id"""
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return Genre(uuid=genre.uuid, name=genre.name)
