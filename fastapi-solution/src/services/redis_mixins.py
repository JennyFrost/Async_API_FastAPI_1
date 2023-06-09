import json
from typing import Optional
from pydantic import BaseModel
from redis.asyncio import Redis
from elasticsearch import AsyncElasticsearch


class MainServiceMixin:

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic


class CacheMixin(MainServiceMixin):

    async def _object_from_cache(self, some_id: str) -> Optional[str]:
        data = await self.redis.get(some_id)
        if not data:
            return None
        return data
    
    async def _objects_from_cache(self, some_id: str) -> Optional[dict]:
        data = await self.redis.get(some_id)
        if not data:
            return []
        objects = json.loads(data)
        return objects

    async def _put_object_to_cache(self, object: BaseModel, some_id: str, time_cache: int=30):
        await self.redis.set(some_id, object.json(), time_cache)

    async def _put_objects_to_cache(self, objects: list[BaseModel], some_id: str, time_cache: int=60):
        objects = [object.json() for object in objects]
        objects = json.dumps(objects)
        await self.redis.set(some_id, objects, time_cache)