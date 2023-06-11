import os

from pydantic import BaseModel

from dotenv import load_dotenv

load_dotenv()


class DSL(BaseModel):
    dbname: str = os.environ.get('DB_NAME')
    user: str = os.environ.get('DB_USER')
    password: str = os.environ.get('DB_PASSWORD')
    host: str = os.environ.get('DB_HOST')
    port: str = os.environ.get('DB_PORT')


class ES(BaseModel):
    host: str = os.environ.get('ES_HOST')
    port: str = os.environ.get('ES_PORT')


dsl = DSL().dict()

es = ES().dict()

limit = 100

index_name = 'persons'

default_index = {
            "settings": {
                "refresh_interval": "1s",
                "analysis": {
                    "filter": {
                        "english_stop": {
                            "type": "stop",
                            "stopwords": "_english_"
                        },
                        "english_stemmer": {
                            "type": "stemmer",
                            "language": "english"
                        },
                        "english_possessive_stemmer": {
                            "type": "stemmer",
                            "language": "possessive_english"
                        },
                        "russian_stop": {
                            "type": "stop",
                            "stopwords": "_russian_"
                        },
                        "russian_stemmer": {
                            "type": "stemmer",
                            "language": "russian"
                        }
                    },
                    "analyzer": {
                        "ru_en": {
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "english_stop",
                                "english_stemmer",
                                "english_possessive_stemmer",
                                "russian_stop",
                                "russian_stemmer"
                            ]
                        }
                    }
                }
            },
            "mappings": {
                "dynamic": "strict",
                "properties": {
                    "uuid": {
                        "type": "keyword"
                    },
                    "full_name": {
                        "type": "text",
                        "analyzer": "ru_en",
                    },
                }
            }
        }
