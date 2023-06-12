from models.base_config import BaseOrjsonModel


class Genre(BaseOrjsonModel):
    uuid: str
    name: str
