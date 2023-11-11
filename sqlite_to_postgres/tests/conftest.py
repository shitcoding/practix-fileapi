import os
import sqlite3

import psycopg2
import pytest
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

from load_data import dict_factory


@pytest.fixture(scope="class", autouse=True)
def connect_to_postgresql(request):
    load_dotenv()
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': int(os.environ.get('DB_PORT', 5432)),
        'options': '-c search_path=public,content'
    }
    request.cls.pg_conn = psycopg2.connect(**dsl, cursor_factory=RealDictCursor)


@pytest.fixture(scope="class", autouse=True)
def connect_to_sqlite(request):
    load_dotenv()
    request.cls.sqlite_conn = sqlite3.connect(os.environ.get('SQLITE_DB_PATH'))
    request.cls.sqlite_conn.row_factory = dict_factory



