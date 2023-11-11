import logging
import os
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

LIMIT = 100

load_dotenv()

DEBUG = os.environ.get('DEBUG', False) == 'True'

SCHEMA = 'content'

DSN = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': os.environ.get('DB_PORT', 5432),
    'options': '-c search_path=public,content',
}

ES_SERVER = os.environ.get('ES_SERVER')

logger = logging.getLogger()

if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

try:
    os.mkdir('logs')
except FileExistsError:
    pass

if DEBUG:
    fh = StreamHandler()
else:
    fh = RotatingFileHandler('logs/etl_logs.log', maxBytes=5000000, backupCount=5)

formatter = logging.Formatter('%(asctime)s %(levelname)-8s [%(filename)-16s:%(lineno)-5d] %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)

