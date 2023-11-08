import sqlite3
from contextlib import contextmanager

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from db_settings import CHUNK_SIZE, DSL, SQLITE_DB_PATH
from etl import ETL
from extraction import SQLiteExtractor
from loading import PostgresLoader


def dict_factory(cursor: sqlite3.Cursor, row: tuple) -> dict:
    dictionary = {}
    for idx, col in enumerate(cursor.description):
        dictionary[col[0]] = row[idx]
    return dictionary


@contextmanager
def sqlite_conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    yield conn
    conn.close()


@contextmanager
def pg_conn_context(dsl: dict):
    conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    yield conn
    conn.close()


def load_from_sqlite(lite_conn: sqlite3.Connection,
                     pg_conn: _connection,
                     chunk_size: int = 100) -> None:
    """Основной метод загрузки данных из SQLite в Postgres"""

    postgres_saver = PostgresLoader(pg_conn)
    sqlite_extractor = SQLiteExtractor(lite_conn)

    ETL(sqlite_extractor, postgres_saver).save_all_data(chunk_size)


if __name__ == '__main__':

    with sqlite_conn_context(SQLITE_DB_PATH) as sqlite_conn,\
         pg_conn_context(DSL) as pg_conn:

        load_from_sqlite(sqlite_conn, pg_conn, CHUNK_SIZE)

