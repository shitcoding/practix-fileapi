import logging

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
    assert body['name'] == TEST_GENRE_DATA[3].get('name')


@pytest.mark.asyncio
async def test_genre_by_name(make_get_request):

    genre = TEST_GENRE_DATA[3]['name']
    response = await make_get_request(
        path=f'genres/',
        query_data={'name': genre}
    )

    status = response.get('status')
    body = response.get('body')
    assert status == 200
    assert body[0]['name'] == TEST_GENRE_DATA[3].get('name')


@pytest.mark.asyncio
async def test_all_genre(make_get_request):
    response = await make_get_request(
        path='genres/'
    )

    status = response.get('status')
    body = response.get('body')
    assert status == 200
    assert len(body) == len(TEST_GENRE_DATA)