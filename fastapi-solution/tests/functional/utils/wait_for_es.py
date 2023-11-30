import time

from elasticsearch import ConnectionError, Elasticsearch, NotFoundError

from functional.logger import logger
from functional.settings import get_settings

settings = get_settings()

if __name__ == '__main__':
    es_client = Elasticsearch(
        f'http://{settings.elastic.es_host}:{settings.elastic.es_port}'
    )

    while True:
        try:
            if es_client.ping():
                logger.info("Elasticsearch is up and running!")
                break
        except (ConnectionError, NotFoundError):
            logger.info("Waiting for Elasticsearch...")
            time.sleep(1)
