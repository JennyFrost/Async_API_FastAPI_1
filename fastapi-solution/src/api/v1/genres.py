from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from services.genre import GenreService, get_genres_service
from .api_models import Genre

router = APIRouter()


@router.get('/', response_model=list[Genre])
async def list_genre(genre_service: GenreService = Depends(get_genres_service)) -> list[Genre]:
    genres = await genre_service.get_genres_list()
    return [Genre(uuid=genre.uuid, name=genre.name) for genre in genres]