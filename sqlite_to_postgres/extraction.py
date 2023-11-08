import sqlite3
from contextlib import closing
from datetime import datetime
from typing import List

from sqlite_data import (FilmWork, Genre, GenreFilmWork, Person,
                         PersonFilmWork, tables)

DATETIME_MASK = '%Y-%m-%d %H:%M:%S.%f%z'


def _transform_date_fields(sqlite_rec: dict) -> dict:
    init_row = {}
    for key, value in sqlite_rec.items():
        if key == 'created_at':
            init_row['created'] = datetime.strptime(sqlite_rec[key] + '00', DATETIME_MASK)
        elif key == 'updated_at':
            init_row['modified'] = datetime.strptime(sqlite_rec[key] + '00', DATETIME_MASK)
        elif key == 'creation_date':
            init_row[key] = None
            if sqlite_rec[key] is not None:
                init_row[key] = datetime.strptime(sqlite_rec[key] + '00', DATETIME_MASK)

        else:
            init_row[key] = sqlite_rec[key]
    return init_row


class SQLiteExtractor:
    def __init__(self, connection: sqlite3.Connection):
        self._conn = connection

    def extract_table(self, table_name: str, limit: int, offset: int) \
            -> List[Genre | Person | FilmWork | GenreFilmWork | PersonFilmWork]:
        class_inst = tables[table_name]
        records = []
        with closing(self._conn.cursor()) as cursor:
            cursor.execute(f"""SELECT DISTINCT * FROM {table_name} LIMIT {limit} OFFSET {offset}""")
            rows = cursor.fetchall()

        for row in rows:
            init_row = _transform_date_fields(row)
            record = class_inst(**init_row)
            records.append(record)
        return records

    def get_size_table(self, table_name: str) -> int:
        with closing(self._conn.cursor()) as cursor:

            cursor.execute(f"""SELECT count(id) FROM {table_name}""")
            row = cursor.fetchone()
        return row['count(id)']


