import logging
from http import HTTPStatus

import pytest

from functional.testdata.genre_data import TEST_GENRE_DATA


@pytest.mark.asyncio
async def test_genre_by_id(make_get_request):

    genre_uuid = TEST_GENRE_DATA[3]['uuid']
    response = await make_get_request(
        path=f'genres/{genre_uuid}/'
    )

    status = response.get('status')
    body = response.get('body')
    assert status == 200
    assert body['uuid'] == genre_uuid
    assert body['name'] == TEST_GENRE_DATA[3]['name']


@pytest.mark.asyncio
async def test_genre_by_name(make_get_request):

    genre = TEST_GENRE_DATA[3]['name']
    response = await make_get_request(
        path=f'genres/',
        query_data={'name': genre}
    )

    status = response.get('status')
    body = response.get('body')
    assert status == HTTPStatus.OK
    assert body[0]['name'] == TEST_GENRE_DATA[3]['name']


@pytest.mark.asyncio
async def test_all_genre(make_get_request):
    response = await make_get_request(
        path='genres/'
    )

    status = response.get('status')
    body = response.get('body')
    assert status == HTTPStatus.OK
    assert len(body) == len(TEST_GENRE_DATA)


@pytest.mark.asyncio
async def test_sort_by_name_desc(make_get_request):
    response = await make_get_request(path='genres/', query_data={'sort': '-name'})
    assert response.status == HTTPStatus.OK
    assert (
        response.body[0]['name'] == TEST_GENRE_DATA[0]['name']
    )


@pytest.mark.asyncio
async def test_sort_by_name_asc(make_get_request):
    response = await make_get_request(path='genres/', query_data={'sort': 'name'})
    assert response.status == HTTPStatus.OK
    assert (
        response.body[0]['name'] == TEST_GENRE_DATA[7]['name']
    )


@pytest.mark.asyncio
async def test_sort_by_incorrect_field(make_get_request):
    pass
    #FIXME response = await make_get_request('/genres/?sort=some_wrong_name')
    # assert response.status == HTTPStatus.BAD_REQUEST
    # assert response.body['detail'] == GENRES_NOT_FOUND_MESSAGE


@pytest.mark.asyncio
async def test_list_only_three_genres(make_get_request):
    response = await make_get_request(path='genres/', query_data={'page_size': 3, 'page': 1})
    assert response.status == HTTPStatus.OK
    assert len(response.body) == 3
    #TODO assert by body


@pytest.mark.asyncio
async def test_list_all_query_params(make_get_request):
    response = await make_get_request(
        path='genres/',
        query_data={'page_size': 3, 'page': 2, 'sort': '-name'}
    )
    assert response.status == HTTPStatus.OK
    assert len(response.body) == 3
    #TODO assert by body,assert response.body == GENRES_RESPONSE_SORTED_NAME_DESC[3:6]


@pytest.mark.asyncio
async def test_list_with_search_wrong_name(make_get_request):
    response = await make_get_request('/genre/?query=wrong_name')
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body['detail'] == GENRES_NOT_FOUND_MESSAGE

@pytest.mark.asyncio
async def test_fetch_genre_by_wrong_id(make_get_request):
    response = await make_get_request('/genre/any_string')
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body['detail'] == ITEM_DOESNT_EXIST_MESSAGE


@pytest.mark.asyncio
async def test_redis_stored_data(make_get_request, make_redis_request):
    await make_get_request(f'/genre/{GENRES_RESPONSE[0]["uuid"]}')

    redis_data = await make_redis_request(GENRES_RESPONSE[0]['uuid'])
    item_from_redis = orjson.loads(redis_data)

    assert item_from_redis['name'] == GENRES_RESPONSE[0]['name']
    assert item_from_redis['uuid'] == GENRES_RESPONSE[0]['uuid']