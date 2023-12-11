import backoff
from elasticsearch import Elasticsearch

from functional.logger import logger
from functional.settings import get_settings

settings = get_settings()


@backoff.on_exception(backoff.constant, ConnectionError, interval=3, max_tries=20)
def es_connect():
    logger.info("Waiting for Elasticsearch...")
    es_client = Elasticsearch(
        f'http://{settings.elastic.es_host}:{settings.elastic.es_port}'
    )
    if not es_client.ping():
        raise ConnectionError


if __name__ == '__main__':
    es_connect()
    logger.info("Elasticsearch is up and running!")
