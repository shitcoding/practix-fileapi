from core import config
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
es = AsyncElasticsearch(hosts=[f'{config.ELASTIC_SCHEME}://{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])


async def get_redis() -> Redis:
    client = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
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
