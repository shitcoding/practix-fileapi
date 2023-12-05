import pytest

from functional.logger import logger
from functional.settings import get_settings
from functional.testdata.es_mapping import GENRE_MAPPING


test_settings = get_settings()


@pytest.mark.asyncio
async def test_genre(es_data_loader, make_get_request, genre_data_generator):
    await es_data_loader(
        index_name=test_settings.elastic.es_genres_index,
        data_generator=genre_data_generator,
        mapping=GENRE_MAPPING,
    )
    query_data = {'query': 'Romance'}
    response = await make_get_request(
        path='genres/',
        query_data=query_data,
    )

    status = response.get('status')
    body = response.get('body')
    logger.info(f'answer: {body}')
    assert status == 200
    assert body[0]['name'] == query_data['query']