from dependencies import get_elasticsearch, get_redis
from .elastic_storage import ElasticStorage
from fastapi import Depends
from .base import Cache, Storage
from .redis_cache import RedisCache


def get_cache(client=Depends(get_redis)) -> Cache:
    return RedisCache(redis=client)


def get_storage(client=Depends(get_elasticsearch)) -> Storage:
    return ElasticStorage(elastic_client=client)
