import asyncio

import aiohttp
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from tests.functional.settings import get_settings

settings = get_settings()


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='es_client', scope='session')
async def es_client():
    es_client = AsyncElasticsearch(
        hosts=f'http://{settings.elastic.es_host}:{settings.elastic.es_port}',
        verify_certs=False,
    )
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name='asyncio_client', scope='session')
async def asyncio_client():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(name='es_write_data')
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: list[dict]):
        if await es_client.indices.exists(index=settings.elastic.es_index):
            await es_client.indices.delete(index=settings.elastic.es_index)
        await es_client.indices.create(
            index=settings.elastic.es_index,
            **settings.elastic.es_index_mapping,
        )

        updated, errors = await async_bulk(client=es_client, actions=data)

        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner


@pytest_asyncio.fixture(name='make_get_request')
async def make_get_request(asyncio_client: aiohttp.ClientSession):
    async def inner(path, query_data):
        url = f'http://{settings.fastapi.app_host}:{settings.fastapi.app_port}/api/v1/{path}'

        async with asyncio_client.get(url, params=query_data) as response:
            return {
                'body': await response.json(),
                'headers': response.headers,
                'status': response.status
            }

    return inner
