from pg_work import PostgresLoad
from es_work import ESWriter
from utils import Tools
from state import State
import settings
from time import sleep
from backoff import backoff


@backoff()
def transfer_all_data_from_psql(state):
    """получение и запись данных из postgres и запись в elastic пачками"""
    with PostgresLoad(settings.dsl) as pg_conn:
        data = state.get_last_id_person()
        where_text = ''
        while True:
            if data is not None:
                person_id = data[-1][0]
                where_text = '''where id > '{id}' '''.format(id=person_id)
            data = pg_conn.get_batch_data(limit=settings.limit, where_text=where_text)
            Tools.es_write(data)
            if len(data) < settings.limit:
                break
            state.add_last_id_person(data[-1][0])


@backoff()
def create_index_es():
    """создать индекс для elastic"""
    es = ESWriter(settings.es)
    es.create_index()


@backoff()
def get_updated_movies(state):
    """достать все обновленные фильмы"""
    last_request_date = state.get_datetime_last_request()
    with PostgresLoad(settings.dsl) as pg_conn:
        where_text = '''where (modified > '{date}') ''' \
            .format(
            date=last_request_date
        )
        data = state.get_last_id_person()
        while True:
            if data is not None:
                person_id = data[-1][0]
                where_text = where_text + '''AND id > '{id}' '''.format(id=person_id)
            data = pg_conn.get_batch_data(limit=settings.limit, where_text=where_text)
            if len(data) > 0:
                Tools.es_write(data)
                state.add_last_id_person(data[-1][0])
            if len(data) < settings.limit:
                break


@backoff()
def test_system():
    PostgresLoad(settings.dsl)
    ESWriter(settings.es).get_info()


if __name__ == '__main__':
    #ожидание системы когда БД заработает
    while True:
        success = test_system()
        if success:
            break
    #подготовка переменных состояния
    state = State('state.json')
    state.check_exists()
    state_data = state.read_state()
    if not state_data.get('first_request_bool', False):
        #перенос данных первый раз в пустой индекс
        create_index_es()
        while True:
            success = transfer_all_data_from_psql(state=state)
            if success:
                break
        state.update_state({'first_request_bool': True, 'last_id_person': None})
    # постоянная подгрузка данных
    while True:
        success = get_updated_movies(state=state)
        if success:
            state.update_datetime_last_request()
            state.add_last_id_person(None)
        sleep(10)
