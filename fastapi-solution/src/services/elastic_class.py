from elasticsearch import AsyncElasticsearch, NotFoundError
from pydantic import BaseModel


class ElasticMain:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_obj_from_elastic(self, id: str, index: str, some_class) -> BaseModel | None:
        try:
            doc = await self.elastic.get(index=index, id=id)
        except NotFoundError:
            return None
        return some_class(**doc['_source'])