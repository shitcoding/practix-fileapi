from redis.asyncio import Redis
from elasticsearch import AsyncElasticsearch

from core import config

redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
es = AsyncElasticsearch(hosts=[f'{config.ELASTIC_SCHEME}://{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])


async def get_redis() -> Redis:
    client = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    try:
        yield client
    finally:
        await client.close()


async def get_elasticsearch() -> AsyncElasticsearch:
    client = AsyncElasticsearch(hosts=[f'{config.ELASTIC_SCHEME}://{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])
    try:
        yield client
    finally:
        await client.close()
