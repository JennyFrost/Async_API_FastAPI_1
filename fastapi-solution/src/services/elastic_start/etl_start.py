from utils import load_env, DslEl, StoragePlace, JsonFileStorage
from elastic import ElasticMain

class ETL:
    def __init__(self, elastic_dsl: DslEl, storage_place: StoragePlace):
        self.elastic_dsl = elastic_dsl
        self.storage_place = storage_place
        self.index_json = JsonFileStorage(storage_place.index_path)
        self.dump_json = JsonFileStorage(storage_place.dump_path)

    def worker(self):
        el_manage = ElasticMain(**self.elastic_dsl.dict())

        if not el_manage.check_index():
            el_manage.create_index(self.index_json.retrieve_state())
            dump = self.dump_json.retrieve_state()
            el_manage.bulk_load(dump)
        
    def __call__(self):
        self.worker()

if __name__ == "__main__":
    dsl, str_places = load_env()
    etl = ETL(dsl, str_places)
    etl()