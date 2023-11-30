import pytest
from tests.functional.settings import get_settings
from tests.functional.testdata.es_mapping import MOVIE_MAPPING

test_settings = get_settings()


@pytest.mark.asyncio
async def test_search(es_data_loader, make_get_request, movie_data_generator):
    await es_data_loader(
        index_name=test_settings.elastic.es_movies_index,
        data_generator=movie_data_generator,
        mapping=MOVIE_MAPPING,
    )
    query_data = {'query': 'The Star'}
    response = await make_get_request(
        path='films/search',
        query_data=query_data,
    )

    status = response.get('status')
    body = response.get('body')

    assert status == 200
    assert len(body) == 50
