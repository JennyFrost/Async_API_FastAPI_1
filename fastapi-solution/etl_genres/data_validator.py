import uuid
from pydantic import BaseModel


class Genre(BaseModel):
    id: uuid.UUID
    name: str

    def to_es_format(self, index_name: str) -> list[dict]:
        es_dict1 = {
                    "index":
                            {
                             '_index': index_name,
                             '_id': self.id
                             }
                   }
        es_dict2 = {
                    'uuid': str(self.id),
                    'name': self.name
                    }
        return [es_dict1, es_dict2]