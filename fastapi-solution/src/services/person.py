from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import PersonBase, Role, Person, PersonFilm

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 2


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        person = await self._person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)
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

    async def _person_from_cache(self, person_id: str) -> Optional[Person]:
        data = await self.redis.get(person_id)
        if not data:
            return None
        person = Person.parse_raw(data)
        return person

    async def _put_person_to_cache(self, person: PersonBase):
        await self.redis.set(person.uuid, person.json(), PERSON_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
