from contextlib import closing
from dataclasses import fields
from typing import List

import psycopg2
from psycopg2.extensions import connection

from sqlite_data import tables


class PostgresLoader:
    def __init__(self, conn: psycopg2.extensions.connection):
        self._conn = conn

    def load_to_table(self, table_name: str, list_records: List) -> None:
        with closing(self._conn.cursor()) as cursor:
            requisites = ', '.join([field.name for field in fields(tables[table_name])])

            parts = [item.to_str_tuple() for item in list_records]

            data_to_insert = []
            for part in parts:
                data = cursor.mogrify("(" + ", ".join(["%s" for _ in range(len(part))]) + ")", part).decode()
                data_to_insert.append(data)

            args = ','.join(data_to_insert)
            cursor.execute(
                f"""INSERT INTO {table_name}({requisites}) 
                    VALUES {args} 
                    ON CONFLICT DO NOTHING""")
        self._conn.commit()
