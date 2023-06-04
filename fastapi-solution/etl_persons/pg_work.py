import psycopg2
from psycopg2.extras import DictCursor


MAIN_SQL = '''SELECT
               id,
               full_name
            FROM content.person
            {where_text}
            ORDER BY id;'''


class PostgresLoad:

    def __init__(self, data):
        self.data = data
        self.conn_pg = psycopg2.connect(**self.data, cursor_factory=DictCursor)

    def close_connect(self) -> None:
        self.conn_pg.close()

    def rollback_connect(self) -> None:
        self.conn_pg.rollback()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close_connect()

    def get_batch_data(self, where_text=None, limit=100):
        if where_text is None:
            where_text = ''
        sql_text =MAIN_SQL.format(where_text=where_text, limit=limit)
        with self.conn_pg.cursor() as pg_cursor:
            pg_cursor.execute(sql_text)
            data = pg_cursor.fetchmany(limit)
        return data


#код для заполнения бд рандомными датами создания фильма
    # def get_all_data(self):
    #     sql = '''
    #     SELECT film_work.id FROM content.film_work;'''
    #     with self.conn_pg.cursor() as pg_cursor:
    #         pg_cursor.execute(sql)
    #         id_list = pg_cursor.fetchall()
    #     return id_list
    #
    # def update_data(self, id_film):
    #     sql = '''
    #     UPDATE content.film_work
    #     SET creation_date = '{date}'
    #     where id = '{id_film}';
    #     '''.format(date=self.random_date(), id_film=id_film)
    #     with self.conn_pg.cursor() as pg_cursor:
    #         pg_cursor.execute(sql)
    #     self.conn_pg.commit()
    #
    # def random_date(self):
    #     start = datetime(1980,2,15).timestamp()
    #     end = datetime(2022,12,31).timestamp()
    #     timedelta = end - start
    #     start = start + random.randint(0, timedelta)
    #     start = datetime.fromtimestamp(start).date()
    #     return str(start)


