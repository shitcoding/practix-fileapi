import logging

import pytest_asyncio
from tests.functional.settings import get_settings
from tests.functional.testdata.es_mapping import GENRE_MAPPING
from tests.functional.testdata.genre_data import TEST_GENRE_DATA

test_settings = get_settings()


@pytest_asyncio.fixture(scope='session')
def genre_data_generator():
    def generate_data():
        return TEST_GENRE_DATA
    return generate_data


@pytest_asyncio.fixture(scope='session')
async def genre_to_es(es_data_loader, genre_data_generator):
    logging.info('Loading genres to ES...')
    await es_data_loader(
        index_name=test_settings.elastic.es_genres_index,
        data_generator=genre_data_generator,
        mapping=GENRE_MAPPING,
    )
