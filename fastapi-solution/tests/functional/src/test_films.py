import pytest

from tests.functional.testdata.es_mapping import MOVIE_MAPPING
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
    assert response['status'] == 200
    assert isinstance(response['body'], list)


@pytest.mark.asyncio
async def test_get_similar_films(es_data_loader, make_get_request, movie_data_generator):
    await es_data_loader(
        index_name=test_settings.elastic.es_movies_index,
        data_generator=movie_data_generator,
        mapping=MOVIE_MAPPING,
    )

    valid_film_id = "e42d300d-d671-4877-aa3f-d7fb1ced52ad"
    response = await make_get_request(f'films/{valid_film_id}/similar', {})
    assert response['status'] == 200
    assert isinstance(response['body'], list)


@pytest.mark.asyncio
async def test_search_films(es_data_loader, make_get_request, movie_data_generator):
    await es_data_loader(
        index_name=test_settings.elastic.es_movies_index,
        data_generator=movie_data_generator,
        mapping=MOVIE_MAPPING,
    )

    query = "The Star"
    response = await make_get_request('films/search', {"query": query})
    assert response['status'] == 200
    assert isinstance(response['body'], list)


@pytest.mark.asyncio
async def test_film_details(es_data_loader, make_get_request, movie_data_generator):
    await es_data_loader(
        index_name=test_settings.elastic.es_movies_index,
        data_generator=movie_data_generator,
        mapping=MOVIE_MAPPING,
    )

    valid_film_id = "e42d300d-d671-4877-aa3f-d7fb1ced52ad"
    response = await make_get_request(f'films/{valid_film_id}', {})
    assert response['status'] == 200
    assert isinstance(response['body'], dict)

    invalid_film_id = "e42d300d-d671-4877-aa3f-d7fb1ced523232"
    response = await make_get_request(f'films/{invalid_film_id}', {})
    assert response['status'] == 404
