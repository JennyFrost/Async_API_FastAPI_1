from inspect_data import DataToES
from es_work import ESWriter
from settings import es, index_name


class Tools:

    @classmethod
    def es_write(cls, data):
        data_for_write_to_es = cls.formatting_data(data)
        ESWriter(es).bulk_create_data(data_for_write_to_es)

    @classmethod
    def formatting_data(cls, data):
        data_for_write_to_es = []
        for item_data in data:
            item_data = dict(zip(('id', 'full_name'), item_data))
            item_data = DataToES(**item_data).json_dict(index=index_name)
            data_for_write_to_es.append(item_data)
        return data_for_write_to_es
