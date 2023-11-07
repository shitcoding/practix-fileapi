import sqlite3
import psycopg2
import uuid
import datetime
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from dataclasses import dataclass, field, fields, astuple
from typing import ClassVar as Meta


@dataclass(frozen=True)
class UUIDMixin:
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class CreatedAtMixin:
    created_at: datetime.datetime


@dataclass(frozen=True)
class ModifiedAtMixin:
    updated_at: datetime.datetime


@dataclass(frozen=True)
class FullMixin(UUIDMixin, CreatedAtMixin, ModifiedAtMixin):
    pass


@dataclass(frozen=True)
class IdCreatedMixin(UUIDMixin, CreatedAtMixin):
    pass


@dataclass(frozen=True)
class Person(FullMixin):
    table_name: Meta = "Person"
    full_name: str = ""


@dataclass(frozen=True)
class Genre(FullMixin):
    table_name: Meta = "Genre"
    name: str = ""
    description: str = ""


@dataclass(frozen=True)
class Film_work(FullMixin):
    table_name: Meta = "film_work"
    title: str = ""
    description: str = ""
    type: str = ""
    rating: float = field(default=0.0)
    creation_date: datetime.datetime = datetime.datetime.now()
    file_path: str = ""
    certificate: str = ""


@dataclass(frozen=True)
class Person_film_work(IdCreatedMixin):
    table_name: Meta = "person_film_work"
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    role: str = ""


@dataclass(frozen=True)
class Genre_film_work(IdCreatedMixin):
    table_name: Meta = "genre_film_work"
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)


class PostgresSaver:
    def __init__(self, pg_conn: _connection) -> None:
        self.curs = pg_conn.cursor()

    def save_all_data(self, table, in_row):
        temp_dict = dict(in_row)
        if 'file_path' in temp_dict.keys() and not temp_dict['file_path']:
            temp_dict['file_path'] = ''
        convert_obj = table(**temp_dict)
        columns = [field.name for field in fields(convert_obj)]
        column_names = ",".join(columns)
        column_placeholders = ",".join(["%s"] * len(columns))
        bind_values = self.curs.mogrify(column_placeholders,
                                        astuple(convert_obj)).decode("utf-8")
        query = (
            f"INSERT INTO content.{table.table_name} "
            f"({column_names}) VALUES ({bind_values})"
            f" ON CONFLICT DO NOTHING"
        )
        self.curs.execute(query)


class SQLiteExtractor:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.curs = connection.cursor()

    def extract_movies(self, table, n=1000):
        self.curs.execute(f"select * from {table.table_name}")
        while True:
            data = self.curs.fetchmany(n)
            if data:
                yield from data
            else:
                break


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    tables = (Person, Genre, Film_work, Person_film_work, Genre_film_work)
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)
    for table in tables:
        for data in sqlite_extractor.extract_movies(table):
            postgres_saver.save_all_data(table, data)


def convert_date(val):
    return datetime.datetime.fromisoformat(val.decode())


if __name__ == "__main__":
    sqlite3.register_converter("timestamp", convert_date)
    dsl = {
        "dbname": "movies_database",
        "user": "app",
        "password": "123qwe",
        "host": "db",
        "port": 5432,
    }
    with sqlite3.connect(
        "/in_data/db.sqlite", detect_types=sqlite3.PARSE_DECLTYPES
    ) as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor
                                       ) as pg_conn:
        sqlite_conn.row_factory = sqlite3.Row
        load_from_sqlite(sqlite_conn, pg_conn)
    sqlite_conn.close()
    pg_conn.close()
