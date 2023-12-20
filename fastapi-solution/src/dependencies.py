from redis.asyncio import Redis
from elasticsearch import AsyncElasticsearch

from core.config import settings

redis = Redis(host=settings.redis.redis_host, port=settings.redis.redis_port)
es = AsyncElasticsearch(hosts=[f'{settings.elastic.es_scheme}://{settings.elastic.es_host}:{settings.elastic.es_port}'])


async def get_redis() -> Redis:
    client = Redis(host=settings.redis.redis_host, port=settings.redis.redis_port)
    try:
        yield client
    finally:
        await client.close()


async def get_elasticsearch() -> AsyncElasticsearch:
    elastic_host = f'{settings.elastic.es_scheme}://{settings.elastic.es_host}:{settings.elastic.es_port}'
    client = AsyncElasticsearch(hosts=[elastic_host])
    try:
        yield client
    finally:
        await client.close()
