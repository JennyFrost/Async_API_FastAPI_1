# Классы для работы с ElasticSearch

from elasticsearch import Elasticsearch, helpers
from log_pack import log_error, log_success
from utils import backoff


class ElasticMain:
    """Управляющий класс Elasticsearch"""

    def __init__(self, host: str, port: str):
        self.dsl = f"http://{host}:{port}"
        self.client = self.elastic_client(self.dsl)

    @backoff()
    @staticmethod
    def elastic_client(dsl: str) -> Elasticsearch:
        """Метод для подключения к elasticsearch"""

        try:
            es_client = Elasticsearch(dsl)
            if es_client.ping():
                log_success("Elastic connection successfully completed")
                return es_client
            log_error("Failed connect to Elastic")
        except Exception as err:
            log_error(err)

    def create_index(self, index: dict) -> bool:
        """Метод создает индекс, если индекс создать невозможно то программа закрывается"""

        self.client.indices.create(index="movies", ignore=400, body=index)
        log_success("index is created")
        return True

    def bulk_load(self, data: list):
        """Метод записывает данные в индекс пачками"""

        helpers.bulk(self.client, data)

    def check_index(self) -> bool:
        """Проверяет есть ли индекс"""

        res = self.client.indices.exists(index="movies")
        return res

    def count_items_index(self) -> int:
        """Возвращает количество элементов в индексе"""

        resp = self.client.count(index="movies").body["count"]
        return resp

    def del_index(self) -> bool:
        """Метод для удаления индекса, вернет true если индекс удален"""

        self.client.delete(index="movies")
        return True
