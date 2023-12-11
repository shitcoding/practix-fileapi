from http import HTTPStatus

import pytest
from tests.functional.testdata.genre_data import TEST_GENRE_DATA


@pytest.mark.asyncio
@pytest.mark.usefixtures("genre_to_es")
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
@pytest.mark.usefixtures("genre_to_es")
async def test_genre_by_name(make_get_request):

    genre = TEST_GENRE_DATA[3]['name']
    response = await make_get_request(
        path='genres/',
        query_data={'query': genre}
    )

    assert response['status'] == HTTPStatus.OK
    assert response['body'][0]['name'] == TEST_GENRE_DATA[3]['name']


@pytest.mark.asyncio
@pytest.mark.usefixtures("genre_to_es")
async def test_all_genre(make_get_request):
    response = await make_get_request(
        path='genres/'
    )

    assert response['status'] == HTTPStatus.OK
    assert len(response['body']) == len(TEST_GENRE_DATA)


@pytest.mark.asyncio
@pytest.mark.usefixtures("genre_to_es")
async def test_list_with_search_wrong_name(make_get_request):
    response = await make_get_request(
        path='genres/',
        query_data={'query': 'wrong_name'}
    )
    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.usefixtures("genre_to_es")
async def test_fetch_genre_by_wrong_id(make_get_request):
    response = await make_get_request('genres/any_string')
    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.usefixtures("genre_to_es")
async def test_redis_stored_data(make_get_request):
    # Делаем запрос к ES = кэшируем ответ
    await make_get_request(f'genres/{TEST_GENRE_DATA[2]["uuid"]}')
    # Получаем данные из Redis
    response = await make_get_request(path=f'genres/{TEST_GENRE_DATA[2]["uuid"]}')
    assert response['status'] == HTTPStatus.OK
    assert response['body']['name'] == TEST_GENRE_DATA[2]['name']
    assert response['body']['uuid'] == TEST_GENRE_DATA[2]['uuid']
