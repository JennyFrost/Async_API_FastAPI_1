from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from settings import default_index, index_name


class ESWriter:
    def __init__(self, data):
        self.es = Elasticsearch(f'http://{data["host"]}:{data["port"]}')

    def create_index(self):
        if self.es.indices.exists(index=index_name):
            self.es.indices.delete(index=index_name)
        self.es.indices.create(index=index_name, body=default_index)

    def bulk_create_data(self, data):
        bulk(self.es, data)

    def get_info(self):
        return self.es.info()
