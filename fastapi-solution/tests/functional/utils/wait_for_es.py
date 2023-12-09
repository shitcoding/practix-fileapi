import time
import backoff 
from elasticsearch import ConnectionError, Elasticsearch, NotFoundError

from functional.logger import logger
from functional.settings import get_settings

settings = get_settings()

@backoff.on_exception(backoff.constant,(ConnectionError, NotFoundError),max_tries=5)
def es_ping(client):
    logger.info("Waiting for Elasticsearch...")
    client.ping()
    

if __name__ == '__main__':
    es_client = Elasticsearch(
        f'http://{settings.elastic.es_host}:{settings.elastic.es_port}'
    )
    es_ping(es_client)
    logger.info("Elasticsearch is up and running!")

