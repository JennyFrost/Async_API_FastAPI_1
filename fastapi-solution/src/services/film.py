import json
from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film, FilmBase

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def get_person_films(self, person_id: str) -> Optional[list[FilmBase]]:
        person_films = await self._person_films_from_cache(person_id)
        if not person_films:
            person_films = await self._get_person_films_from_elastic(person_id)
            if not person_films:
                return []
            await self._put_person_films_to_cache(person_films, person_id)
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
                  "_source": ["id", "title", "imdb_rating"],
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

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None

        film = Film.parse_raw(data)
        return film

    async def _person_films_from_cache(self, person_id: str) -> Optional[list[FilmBase]]:
        data = await self.redis.get('person_films_' + person_id)
        if not data:
            return None
        films = json.loads(data)
        films = [FilmBase.parse_raw(film) for film in films]
        return films

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.id, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_person_films_to_cache(self, films: list[FilmBase], person_id: str):
        films = [film.json() for film in films]
        films = json.dumps(films)
        await self.redis.set('person_films_' + person_id, films, FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
