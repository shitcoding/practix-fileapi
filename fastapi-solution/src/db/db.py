from fastapi import Depends

from dependencies import get_elasticsearch
from .elastic_storage import ElasticStorage
from .base import Cache, Storage
from .redis_cache import RedisCache


def get_cache(**kwargs) -> Cache:
    return RedisCache(**kwargs)


def get_storage(client=Depends(get_elasticsearch)) -> Storage:
    return ElasticStorage(elastic_client=client)
