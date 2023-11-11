from .elastic_storage import ElasticStorage
from .base import Cache, Storage
from .redis_cache import RedisCache


def get_cache(**kwargs) -> Cache:
    return RedisCache(**kwargs)


def get_storage(**kwargs) -> Storage:
    return ElasticStorage(**kwargs)
