from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre

from services.redis_mixins import CacheMixin


GENRES_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class GenreService(CacheMixin):

    async def get_genres_list(self) -> Optional[list[Genre]]:
        genres = await self._objects_from_cache('all_genres')
        if not genres:
            genres = await self._get_genres_from_elastic()
            if not genres:
                return []
            await self._put_objects_to_cache(genres, 'all_genres')
        return genres

    async def _get_genres_from_elastic(self) -> Optional[list[Genre]]:
        try:
            genres = await self.elastic.search(index='genres', body={"query": {"match_all": {}}})
        except NotFoundError:
            return None
        return [Genre(**genre['_source']) for genre in genres['hits']['hits']]
    
    async def _objects_from_cache(self, some_id: str) -> Optional[list[Genre]]:
        objects = await super()._objects_from_cache(some_id)
        genres = [Genre.parse_raw(obj) for obj in objects]
        return genres
    
    async def _object_from_cache(self, some_id: str) -> Optional[Genre]:
        obj = await super()._object_from_cache(some_id)
        genre = Genre.parse_raw(obj)
        return genre


@lru_cache()
def get_genres_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
