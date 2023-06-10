from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis

from models.film import Film, FilmBase
from services.redis_mixins import CacheMixin


FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService(CacheMixin):

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._object_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_object_to_cache(film, film_id)

        return film

    async def get_person_films(self, person_id: str) -> Optional[list[FilmBase]]:
        person_films = await self._objects_from_cache('person_films_' + person_id)
        if not person_films:
            person_films = await self._get_person_films_from_elastic(person_id)
            if not person_films:
                return []
            await self._put_objects_to_cache(person_films, 'person_films_' + person_id)
        return person_films

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get(index='movies', id=film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _get_person_films_from_elastic(self, person_id: str) -> Optional[list[FilmBase]]:
        films = await self.elastic.search(
            index='movies',
            body={
                "_source": [
                    "id",
                    "title",
                    "imdb_rating"
                ],
                "query": {
                    "bool": {
                        "should": [
                            {
                                "nested": {
                                    "path": "actors",
                                    "query": {
                                        "term": {
                                            "actors.id": person_id
                                        }
                                    }
                                }
                            },
                            {
                                "nested": {
                                    "path": "director",
                                    "query": {
                                        "term": {
                                            "director.id": person_id
                                        }
                                    }
                                }
                            },
                            {
                                "nested": {
                                    "path": "writers",
                                    "query": {
                                        "term": {
                                            "writers.id": person_id
                                        }
                                    }
                                }
                            }
                        ]
                    }
                },
                "sort": [
                    {
                        "imdb_rating": {
                            "order": "desc"
                        }
                    }
                ]
            }
        )
        films = [FilmBase(**film['_source']) for film in films['hits']['hits']]
        return films

    async def _object_from_cache(self, some_id: str) -> Optional[FilmBase]:
        obj = await super()._object_from_cache(some_id)
        if obj:
            film = FilmBase.parse_raw(obj)
            return film
    
    async def _objects_from_cache(self, some_id: str) -> list[FilmBase] | []:
        objects = await super()._objects_from_cache(some_id)
        films = [FilmBase.parse_raw(obj) for obj in objects]
        return films


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
