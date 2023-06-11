from utils import load_env, DslEl, StoragePlace, JsonFileStorage
from elastic import ElasticMain
from log_pack import log_error, log_success

class ETL:
    def __init__(self, elastic_dsl: DslEl, storage_place: StoragePlace):
        self.elastic_dsl = elastic_dsl
        self.index_json = JsonFileStorage(storage_place.index_path)
        self.dump_json = JsonFileStorage(storage_place.dump_path)

    def load_data(self):
        el_manage = ElasticMain(**self.elastic_dsl.dict())

        if not el_manage.check_index():
            try:
                el_manage.create_index(self.index_json.retrieve_state())
                dump = self.dump_json.retrieve_state()
                el_manage.bulk_load(dump)
            except Exception as err:
                log_error(err)
                log_error("Data download failed")

            if el_manage.count_items_index() == 999:
                log_success("Data upload to elasticsearch was completed successfully")
        else:
            log_error("The index has already been created")


if __name__ == "__main__":
    dsl, str_places = load_env()
    etl = ETL(dsl, str_places)
    etl.load_data()