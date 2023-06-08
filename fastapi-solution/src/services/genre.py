from functools import lru_cache
from typing import Optional
import json

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre

GENRES_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_genres_list(self) -> Optional[list[Genre]]:
        genres = await self._genres_from_cache()
        if not genres:
            genres = await self._get_genres_from_elastic()
            if not genres:
                return []
            await self._put_genres_to_cache(genres)
        return genres

    async def _get_genres_from_elastic(self) -> Optional[list[Genre]]:
        try:
            genres = await self.elastic.search(index='genres', body={"query": {"match_all": {}}})
        except NotFoundError:
            return None
        return [Genre(**genre['_source']) for genre in genres['hits']['hits']]

    async def _genres_from_cache(self) -> Optional[list[Genre]]:
        data = await self.redis.get('all_genres')
        if not data:
            return None
        genres = json.loads(data)
        genres = [Genre.parse_raw(genre) for genre in genres]
        return genres

    async def _put_genres_to_cache(self, genres: list[Genre]):
        genres = [genre.json() for genre in genres]
        genres = json.dumps(genres)
        await self.redis.set('all_genres', genres, GENRES_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genres_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
