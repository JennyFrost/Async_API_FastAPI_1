from datetime import date

from pydantic import BaseModel
from uuid import UUID



class DataToES(BaseModel):
    id: UUID
    full_name: str

    def json_dict(self, index):
        item_for_bulk = {
            '_index': index,
            '_id': str(self.id),
            '_source': {
                'uuid': str(self.id),
                'full_name': self.full_name,
            }
        }
        return item_for_bulk
