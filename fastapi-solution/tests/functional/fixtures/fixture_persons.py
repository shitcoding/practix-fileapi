import logging

import pytest_asyncio
from tests.functional.settings import get_settings
from tests.functional.testdata.es_mapping import PERSON_MAPPING, MOVIE_MAPPING
from tests.functional.testdata.person_data import TEST_PERSON_DATA_INDEX, TEST_FILM

test_settings = get_settings()


@pytest_asyncio.fixture(scope='session')
def person_data_generator():
    def generate_data():
        return TEST_PERSON_DATA_INDEX

    return generate_data


@pytest_asyncio.fixture(scope='session')
def film_data_generator():
    def generate_data():
        return TEST_FILM

    return generate_data


@pytest_asyncio.fixture(scope='session')
async def person_to_es(es_data_loader, person_data_generator, film_data_generator):
    logging.info('Loading genres to ES...')
    await es_data_loader(
        index_name=test_settings.elastic.es_movies_index,
        data_generator=film_data_generator,
        mapping=MOVIE_MAPPING,
    )

    await es_data_loader(
        index_name=test_settings.elastic.es_persons_index,
        data_generator=person_data_generator,
        mapping=PERSON_MAPPING,
    )
