import os

from dotenv import load_dotenv

load_dotenv()
DSL = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': os.environ.get('DB_PORT', 5432),
    'options': '-c search_path=public,content',
}

SQLITE_DB_PATH = os.environ.get('SQLITE_DB_PATH', 'db.sqlite')
CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE'))
