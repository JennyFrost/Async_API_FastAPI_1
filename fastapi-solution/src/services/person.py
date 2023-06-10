from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Role, Person, PersonFilm
from services.redis_mixins import CacheMixin

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 2


class PersonService(CacheMixin):

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        person = await self._object_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_object_to_cache(person, person_id)
        return person

    async def _get_person_from_elastic(self, person_id: str) -> Optional[Person]:
        try:
            doc = await self.elastic.get(index='persons', id=person_id)
            films = await self.elastic.search(
                index='movies',
                body={
                 "_source": ["id"],
                 "query": {
                   "bool": {
                     "should": [
                       {
                         "nested": {
                           "path": "actors",
                           "query": {
                             "term": {
                               "actors.id": doc['_source']['uuid']
                             }
                           },
                           "inner_hits": {}
                         }
                       },
                         {
                             "nested": {
                                 "path": "director",
                                 "query": {
                                     "term": {
                                         "director.id": doc['_source']['uuid']
                                     }
                                 },
                                 "inner_hits": {}
                             }
                         },
                       {
                         "nested": {
                           "path": "writers",
                           "query": {
                             "term": {
                               "writers.id": doc['_source']['uuid']
                             }
                           },
                           "inner_hits": {}
                         }
                       }
                     ]
                   }
                 }
                }
            )
            person = Person(**doc['_source'])
            for film in films['hits']['hits']:
                film_id = film['_source']['id']
                person_film = PersonFilm(uuid=film_id)
                if film['inner_hits']['actors']['hits']['total']['value'] == 1:
                    person_film.roles.append(Role.actor)
                if film['inner_hits']['writers']['hits']['total']['value'] == 1:
                    person_film.roles.append(Role.writer)
                if film['inner_hits']['director']['hits']['total']['value'] == 1:
                    person_film.roles.append(Role.director)
                person.films.append(person_film)

        except NotFoundError:
            return None
        return person

    async def _object_from_cache(self, some_id: str) -> Optional[Person]:
        obj = await super()._object_from_cache(some_id)
        if obj:
            person = Person.parse_raw(obj)
            return person


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
