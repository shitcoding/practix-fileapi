import uuid

import pytest_asyncio
from tests.functional.settings import get_settings
from tests.functional.testdata.movies_data import TEST_MOVIE_DATA, FIRST_MOVIE_ID

test_settings = get_settings()


@pytest_asyncio.fixture(scope='session')
def movie_data_generator():
    def generate_data():
        data = [{'uuid': FIRST_MOVIE_ID}]
        data[0].update(TEST_MOVIE_DATA)
        for _ in range(59):
            film = {'uuid': uuid.uuid4()}
            film.update(TEST_MOVIE_DATA)
            data.append(film)
        return data

    return generate_data
