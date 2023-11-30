import asyncio
import datetime
import uuid

import aiohttp
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from functional.logger import logger
from tests.functional.settings import get_settings
from tests.functional.testdata.es_mapping import MOVIE_MAPPING

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


@pytest_asyncio.fixture(name='es_data_loader', scope='session')
async def es_data_loader(es_client: AsyncElasticsearch, es_write_data):
    async def inner():
        es_data = [{
            'uuid': str(uuid.uuid4()),
            'imdb_rating': 8.5,
            'genre': ['Action', 'Sci-Fi'],
            'title': 'The Star',
            'description': 'New World',
            'director': ['Stan'],
            'actors_names': ['Ann', 'Bob'],
            'writers_names': ['Ben', 'Howard'],
            'actors': [
                {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'name': 'Ann'},
                {'id': 'fb111f22-121e-44a7-b78f-b19191810fbf', 'name': 'Bob'}
            ],
            'writers': [
                {'id': 'caf76c67-c0fe-477e-8766-3ab3ff2574b5', 'name': 'Ben'},
                {'id': 'b45bd7bc-2e16-46d5-b125-983d356768c6', 'name': 'Howard'}
            ],
            'created_at': datetime.datetime.now().isoformat(),
            'updated_at': datetime.datetime.now().isoformat(),
            'film_work_type': 'movie'
        } for _ in range(60)]

        bulk_query = []
        for row in es_data:
            data = {'_index': 'movies', '_id': row['uuid']}
            data.update({'_source': row})
            bulk_query.append(data)

        await es_write_data(
            data=bulk_query,
            index_mapping=MOVIE_MAPPING,
            elastic_index='movies',
        )
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
