from http import HTTPStatus

import pytest

from tests.functional.testdata.es_mapping import MOVIE_MAPPING
from tests.functional.testdata.movies_data import FIRST_MOVIE_ID
from tests.functional.settings import get_settings

test_settings = get_settings()


@pytest.mark.asyncio
async def test_list_films(es_data_loader, make_get_request, movie_data_generator):
    await es_data_loader(
        index_name=test_settings.elastic.es_movies_index,
        data_generator=movie_data_generator,
        mapping=MOVIE_MAPPING,
    )

    response = await make_get_request(path='films/', query_data={})
    assert response['status'] == HTTPStatus.OK
    assert isinstance(response['body'], list)
    assert len(response['body']) == 10


@pytest.mark.asyncio
async def test_get_similar_films(es_data_loader, make_get_request, movie_data_generator):
    await es_data_loader(
        index_name=test_settings.elastic.es_movies_index,
        data_generator=movie_data_generator,
        mapping=MOVIE_MAPPING,
    )

    valid_film_id = FIRST_MOVIE_ID
    response = await make_get_request(f'films/{valid_film_id}/similar', {})
    assert response['status'] == HTTPStatus.OK
    assert isinstance(response['body'], list)
    assert len(response['body']) == 10


@pytest.mark.asyncio
async def test_search_films(es_data_loader, make_get_request, movie_data_generator):
    await es_data_loader(
        index_name=test_settings.elastic.es_movies_index,
        data_generator=movie_data_generator,
        mapping=MOVIE_MAPPING,
    )

    query = "The Star"
    response = await make_get_request('films/search', {"query": query})
    assert response['status'] == HTTPStatus.OK
    assert isinstance(response['body'], list)
    assert len(response['body']) == 50


@pytest.mark.asyncio
async def test_film_details(es_data_loader, make_get_request, movie_data_generator):
    await es_data_loader(
        index_name=test_settings.elastic.es_movies_index,
        data_generator=movie_data_generator,
        mapping=MOVIE_MAPPING,
    )

    valid_film_id = FIRST_MOVIE_ID
    response = await make_get_request(f'films/{valid_film_id}', {})
    assert response['status'] == HTTPStatus.OK
    assert isinstance(response['body'], dict)
    assert len(response['body']) == 8

    invalid_film_id = f'{FIRST_MOVIE_ID}_invalid'
    response = await make_get_request(f'films/{invalid_film_id}', {})
    assert response.status == HTTPStatus.NOT_FOUND
