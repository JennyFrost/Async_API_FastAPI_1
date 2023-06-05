from uuid import UUID
import psycopg2
from psycopg2.extensions import connection as _connection

from backoff import backoff_break
from etl_logging import logger


class PostgresProducer:

    def __init__(self, time_to_start: str, pg_conn: _connection):
        self.time_to_start = time_to_start
        self.conn = pg_conn
        self.cursor = pg_conn.cursor()
        self.table = 'genre'

    @backoff_break()
    def extract_recs(self, time_to_start: str, was_error: bool = False, recs: list[str] =[]):
        last_date = 0
        if not was_error:
            time_to_start = self.time_to_start
        try:
            query = f'''
                        SELECT id, name, modified 
                        FROM content.{self.table}
                        WHERE modified > '\''{time_to_start}'\''::timestamp with time zone
                        ORDER BY modified 
                    '''
            self.cursor.execute(query)
            new_recs = self.cursor.fetchall()
            if new_recs:
                recs.extend(new_recs)
                last_date = new_recs[-1][1]
        except psycopg2.OperationalError:
            logger.error('Database does not respond! Trying again')
            return 'error', recs, last_date, True
        return recs
