import logging
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID

import backoff
from config.config import LIMIT
from data import ESGenre, ESPerson, FilmWork, Genre, Person, Role
from psycopg2 import OperationalError
from psycopg2.extensions import connection as pg_connection
from psycopg2.extras import DictCursor, DictRow
from psycopg2.pool import ThreadedConnectionPool
from state import State

logger = logging.getLogger(__name__)


@dataclass
class TablesNames:
    genre: str
    person: str
    film_work: str
    person_film_work: str
    genre_film_work: str


class PostgresExtractor:
    @backoff.on_exception(backoff.expo, OperationalError)
    def __init__(self, dsn: dict, schema_name: str, tables_names: TablesNames):
        logger.info('Connect to DB')
        self._dsn = dsn
        self._schema = schema_name
        self._tables = tables_names
        self._pool = ThreadedConnectionPool(
            1, 30,
            database=self._dsn['dbname'],
            user=self._dsn['user'],
            password=self._dsn['password'],
            host=self._dsn['host'],
            port=self._dsn['port'],
            options=self._dsn['options']
        )

    @contextmanager
    def _get_db_connection(self) -> pg_connection:
        connection = None
        try:
            connection = self._pool.getconn()
            yield connection
        finally:
            if connection:
                self._pool.putconn(connection)

    @contextmanager
    def _get_db_cursor(self):
        with self._get_db_connection() as connection:
            cursor = connection.cursor(cursor_factory=DictCursor)
            try:
                yield cursor
            finally:
                cursor.close()

    def _get_ids_changed_records(self, update_date: datetime, table: str, limit: int, offset: int) -> list[
        tuple[str, str]]:
        with self._get_db_cursor() as cursor:
            query = '''SELECT id, modified 
                            FROM {schema}.{table} 
                            WHERE modified > '{update_date}'
                            LIMIT {limit} 
                            OFFSET {offset}'''

            cursor.execute(query.format(schema=self._schema,
                                        table=table,
                                        update_date=update_date,
                                        limit=limit,
                                        offset=offset))
            return cursor.fetchall()

    def _get_ids_dependent_film_works(self, update_date: datetime, table: str, limit: int, offset: int) -> list[
        tuple[str, str]]:
        with self._get_db_cursor() as cursor:
            records_ids = []
            for record in self._get_ids_changed_records(update_date, table, limit, offset):
                records_ids.append(f"'{record[0]}'")

            records_ids_str = ','.join(records_ids)
            if records_ids_str:
                query = '''SELECT fw.id, fw.modified
                                FROM {schema}.{fw_table}  fw
                                LEFT JOIN content.{table}_film_work tfw ON tfw.film_work_id = fw.id
                                WHERE tfw.{table}_id IN ({recs_ids})
                                ORDER BY fw.modified
                                LIMIT {limit}
                                OFFSET {offset};'''

                cursor.execute(query.format(schema=self._schema,
                                            fw_table=self._tables.film_work,
                                            table=table,
                                            recs_ids=records_ids_str,
                                            limit=limit,
                                            offset=offset))
                return cursor.fetchall()
            else:
                return []

    @staticmethod
    def _merge_film_works(film_works: List[DictRow]) -> dict[str, FilmWork]:
        res = {}
        for fw in film_works:
            if not fw['fw_id'] in res:
                film_work = FilmWork(id=UUID(fw['fw_id']), title=fw['title'], description=fw['description'],
                                     rating=fw['rating'], file_path=fw['file_path'])
                res[fw["fw_id"]] = film_work

            if (not fw['person_id'] in res[fw["fw_id"]].persons
                or fw['person_id'] in res[fw["fw_id"]].persons
                and res[fw["fw_id"]].persons[fw['person_id']].role != Role(fw['person_role'])
            ) and fw['person_id'] is not None:
                person = Person(id=UUID(fw['person_id']), name=fw['person_full_name'], role=Role(fw['person_role']))
                res[fw["fw_id"]].persons[fw['person_id']] = person

            if not fw['genre_id'] in res[fw["fw_id"]].genres and fw['genre_id'] is not None:
                genre = Genre(id=UUID(fw['genre_id']), name=fw['genre_name'])
                res[fw["fw_id"]].genres[fw['genre_id']] = genre

        logger.info(f'Extracted {len(res)} movies')
        return res

    @backoff.on_exception(backoff.expo, OperationalError)
    def extract_film_works(self, state: State) -> dict[str, FilmWork]:
        with self._get_db_cursor() as cursor:
            fw_ids = set()
            film_works = self._get_ids_dependent_film_works(update_date=state.update_date,
                                                            table=self._tables.person,
                                                            limit=LIMIT,
                                                            offset=state.offset_person
                                                            )

            film_works.extend(self._get_ids_dependent_film_works(update_date=state.update_date,
                                                                 table=self._tables.genre,
                                                                 limit=LIMIT,
                                                                 offset=state.offset_genre
                                                                 ))
            film_works.extend(self._get_ids_changed_records(update_date=state.update_date,
                                                            table=self._tables.film_work,
                                                            limit=LIMIT,
                                                            offset=state.offset_film_works
                                                            ))
            for fw in film_works:
                # Используются f-строки, так как требуется обернуть id в кавычки
                fw_ids.add(f"'{fw[0]}'")

            fw_ids_str = ','.join(fw_ids)

            if fw_ids_str:
                query = '''SELECT
                                fw.id as fw_id, 
                                fw.title, 
                                fw.description, 
                                fw.rating, 
                                fw.file_path,
                                pfw.role as person_role, 
                                p.id as person_id,  
                                p.full_name as person_full_name,
                                g.id as genre_id,
                                g.name as genre_name
                            FROM {schema}.{fw_table} fw
                            LEFT JOIN {schema}.{pfw_table} pfw ON pfw.film_work_id = fw.id
                            LEFT JOIN {schema}.{p_table} p ON p.id = pfw.person_id
                            LEFT JOIN {schema}.{gfw_table} gfw ON gfw.film_work_id = fw.id
                            LEFT JOIN {schema}.{g_table} g ON g.id = gfw.genre_id
                            WHERE fw.id IN ({recs_ids});'''

                cursor.execute(query.format(schema=self._schema,
                                            fw_table=self._tables.film_work,
                                            p_table=self._tables.person,
                                            g_table=self._tables.genre,
                                            pfw_table=self._tables.person_film_work,
                                            gfw_table=self._tables.genre_film_work,
                                            recs_ids=fw_ids_str))

                rows = cursor.fetchall()
                return PostgresExtractor._merge_film_works(film_works=rows)
            logger.info('All movies have actual state')
            return {}

    @backoff.on_exception(backoff.expo, OperationalError)
    def extract_genres(self, state: State) -> list[ESGenre]:
        with self._get_db_cursor() as cursor:
            genre_ids = set()
            genres = self._get_ids_changed_records(update_date=state.update_date,
                                                   table=self._tables.genre,
                                                   limit=LIMIT,
                                                   offset=state.offset_genre
                                                   )
            for genre in genres:
                # Используются f-строки, так как требуется обернуть id в кавычки
                genre_ids.add(f"'{genre[0]}'")

            genre_ids_str = ','.join(genre_ids)
            res = []
            if genre_ids_str:
                query = '''SELECT
                                g.id as g_id, 
                                g.name as g_name 
                            FROM {schema}.{g_table} g
                            WHERE g.id IN ({recs_ids});'''

                cursor.execute(query.format(schema=self._schema,
                                            g_table=self._tables.genre,
                                            recs_ids=genre_ids_str))

                rows = cursor.fetchall()

                for row in rows:
                    res.append(ESGenre(uuid=row['g_id'], name=row['g_name']))
            logger.info('All genres have actual state')
            return res

    @backoff.on_exception(backoff.expo, OperationalError)
    def extract_persons(self, state: State) -> list[ESPerson]:
        with self._get_db_cursor() as cursor:
            person_ids = set()
            persons = self._get_ids_changed_records(update_date=state.update_date,
                                                    table=self._tables.person,
                                                    limit=LIMIT,
                                                    offset=state.offset_person
                                                    )
            for person in persons:
                # Используются f-строки, так как требуется обернуть id в кавычки
                person_ids.add(f"'{person[0]}'")

            person_ids_str = ','.join(person_ids)
            res = []
            if person_ids_str:
                query = '''SELECT
                                g.id as g_id, 
                                g.full_name as g_name 
                            FROM {schema}.{g_table} g
                            WHERE g.id IN ({recs_ids});'''

                cursor.execute(query.format(schema=self._schema,
                                            g_table=self._tables.person,
                                            recs_ids=person_ids_str))

                rows = cursor.fetchall()

                for row in rows:
                    res.append(ESPerson(uuid=row['g_id'], full_name=row['g_name']))
            logger.info('All persons have actual state')
            return res
