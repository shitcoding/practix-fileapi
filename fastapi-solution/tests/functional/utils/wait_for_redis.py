import backoff
import redis

from functional.logger import logger
from functional.settings import get_settings

settings = get_settings()


@backoff.on_exception(backoff.constant, (redis.exceptions.ConnectionError, redis.exceptions.BusyLoadingError),
                      max_tries=5)
def redis_ping(client):
    logger.info("Waiting for Redis...")
    client.ping()


if __name__ == '__main__':
    redis_host = settings.redis.redis_host
    redis_port = settings.redis.redis_port
    r = redis.Redis(host=redis_host, port=redis_port)
    redis_ping(r)
    logger.info("Redis is up and running!")
