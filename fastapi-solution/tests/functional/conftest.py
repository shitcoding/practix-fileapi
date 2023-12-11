import asyncio
import time
from http import HTTPStatus
from typing import Callable

import aiohttp
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from tests.functional.logger import logger
from tests.functional.settings import get_settings
from tests.functional.testdata.es_mapping import SETTINGS
from urllib3 import HTTPResponse

settings = get_settings()
DataGenerator = Callable[[], list[dict[str, any]]]

pytest_plugins = ['tests.functional.fixtures.fixture_persons',
                  'tests.functional.fixtures.fixture_genres',
                  'tests.functional.fixtures.fixture_movies']


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


@pytest_asyncio.fixture(name='es_data_loader', scope='session')
async def es_data_loader(
        es_client: AsyncElasticsearch,
        es_write_data: Callable,
):
    async def inner(
            index_name: str,
            data_generator: DataGenerator,
            mapping: dict,
    ):
        mapping = {'settings': SETTINGS, 'mappings': mapping}

        es_data = data_generator()
        bulk_query = []
        for row in es_data:
            data = {'_index': index_name, '_id': row['uuid']}
            data.update({'_source': row})
            bulk_query.append(data)

        await es_write_data(
            data=bulk_query,
            index_mapping=mapping,
            elastic_index=index_name,
        )

    return inner


@pytest_asyncio.fixture(name='es_write_data', scope='session')
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: list[dict], index_mapping: dict, elastic_index: str):
        if await es_client.indices.exists(index=elastic_index):
            await es_client.indices.delete(index=elastic_index)
        await es_client.indices.create(
            index=elastic_index,
            **index_mapping,
        )
        updated, errors = await async_bulk(client=es_client, actions=data)

        if errors:
            logger.error(errors)
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner


@pytest_asyncio.fixture(name='make_get_request')
async def make_get_request(asyncio_client: aiohttp.ClientSession):
    async def inner(path: str, query_data: dict = {}) -> dict | HTTPResponse:
        url = f'http://{settings.fastapi.app_host}:{settings.fastapi.app_port}/api/v1/{path}'
        logger.info(url)
        trying = 0
        while trying < 4:
            async with (asyncio_client.get(url, params=query_data) as response):
                logger.info(f'Response status: {response.status}')
                response_json = await response.json()
                time.sleep(0.5)
                if trying == 3:
                    return HTTPResponse(status=HTTPStatus.NOT_FOUND)
                if len(response_json) == 0 or type(response_json) is dict and response_json.get('detail'):
                    trying += 1
                    continue
                return {
                    'body': response_json,
                    'headers': response.headers,
                    'status': response.status
                }

    return inner
