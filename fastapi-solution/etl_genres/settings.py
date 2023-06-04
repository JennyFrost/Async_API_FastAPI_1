from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):

    dbname: str = Field(..., env="PG_NAME")
    user: str = Field(..., env="PG_USER")
    password: str = Field(..., env="PG_PASSWORD")
    host: str = Field(..., env="PG_HOST")
    port: str = Field(..., env="PG_PORT")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class ElasticSettings(BaseSettings):

    scheme: str = Field(..., env="ES_SCHEME")
    host: str = Field(..., env="ES_HOST")
    port: int = Field(..., env="ES_PORT")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


index_name = 'genres'

es_settings = {
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
                    "name": {
                        "type": "text",
                        "analyzer": "ru_en",
                    },
                }
            }
        }
