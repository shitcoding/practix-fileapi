import time

import redis

from functional.logger import logger
from functional.settings import get_settings

settings = get_settings()

if __name__ == '__main__':
    redis_host = settings.redis.redis_host
    redis_port = settings.redis.redis_port
    while True:
        try:
            r = redis.Redis(host=redis_host, port=redis_port)
            if r.ping():
                logger.info("Redis is up and running!")
                break
        except (
                redis.exceptions.ConnectionError,
                redis.exceptions.BusyLoadingError
        ):
            logger.info("Waiting for Redis...")
            time.sleep(1)
