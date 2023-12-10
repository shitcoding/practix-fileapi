import logging
import uuid

import pytest_asyncio
from tests.functional.settings import get_settings
from tests.functional.testdata.movies_data import TEST_MOVIE_DATA

test_settings = get_settings()


@pytest_asyncio.fixture(scope='session')
def movie_data_generator():
    def generate_data():
        data = [{'uuid' : '82a52458-fd52-4313-b124-ccb160c28afb'}]
        data[0].update(TEST_MOVIE_DATA)
        for _ in range(59):
            film = {'uuid' : uuid.uuid4()}
            film.update(TEST_MOVIE_DATA)
            data.append(film)
        return data

    return generate_data
