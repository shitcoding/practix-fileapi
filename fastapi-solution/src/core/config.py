import os
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

ES_SCHEME = os.getenv('ES_SCHEME', 'http')
ES_HOST = os.getenv('ES_HOST', '127.0.0.1')
ES_PORT = int(os.getenv('ES_PORT', 9200))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXPIRE = 60 * 5
DEFAULT_PAGE_SIZE = 10
