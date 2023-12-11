import pytest
from tests.functional.settings import get_settings
from tests.functional.testdata.es_mapping import MOVIE_MAPPING
from http import HTTPStatus
from tests.functional.testdata.person_data import TEST_PERSON_DATA_INDEX

test_settings = get_settings()


@pytest.mark.asyncio
async def test_search(es_data_loader, make_get_request, movie_data_generator):
    await es_data_loader(
        index_name=test_settings.elastic.es_movies_index,
        data_generator=movie_data_generator,
        mapping=MOVIE_MAPPING,
    )
    query_data = {'query': 'Dancing Star'}
    response = await make_get_request(
        path='films/search',
        query_data=query_data,
    )

    status = response.get('status')
    body = response.get('body')

    assert status == HTTPStatus.OK
    assert len(body) == 50


@pytest.mark.asyncio
@pytest.mark.usefixtures("person_to_es")
async def test_list_with_search_wrong_name(make_get_request):
    response = await make_get_request(
        path='persons/search/',
        query_data={'query': 'Rabindranath'}
    )
    assert response['status'] == HTTPStatus.OK
    assert response['body'][0]['uuid'] == TEST_PERSON_DATA_INDEX[0]['uuid']
