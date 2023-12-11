import pytest
from http import HTTPStatus

from tests.functional.testdata.person_data import TEST_PERSON_DATA, FILMS_OF_PERSON


@pytest.mark.asyncio
@pytest.mark.usefixtures("person_to_es")
async def test_person_by_id(make_get_request):
    person_id = TEST_PERSON_DATA[0]['uuid']
    response = await make_get_request(
        path=f'persons/{person_id}'
    )

    assert response['status'] == HTTPStatus.OK
    assert response['body']['uuid'] == TEST_PERSON_DATA[0]['uuid']


@pytest.mark.asyncio
@pytest.mark.usefixtures("person_to_es")
async def test_person_by_name(make_get_request):
    person = TEST_PERSON_DATA[1]['full_name']
    response = await make_get_request(
        path='persons/search/',
        query_data={'query': person.replace(' ', '%20')}
    )

    assert response['status'] == HTTPStatus.OK
    assert response['body'][0]['full_name'] == TEST_PERSON_DATA[1]['full_name']
    assert len(response['body'][0]['films']) == len(TEST_PERSON_DATA[1]['films'])


@pytest.mark.asyncio
@pytest.mark.usefixtures("person_to_es")
async def test_films_of_person(make_get_request):
    person_id = TEST_PERSON_DATA[2]['uuid']
    response = await make_get_request(
        path=f'persons/{person_id}/films'
    )

    assert response['status'] == HTTPStatus.OK
    assert response['body'][0] == FILMS_OF_PERSON[0]
    assert len(response['body']) == len(FILMS_OF_PERSON)


@pytest.mark.asyncio
@pytest.mark.usefixtures("person_to_es")
async def test_all_person(make_get_request):
    response = await make_get_request(
        path='persons/search/'
    )

    assert response['status'] == HTTPStatus.OK
    assert len(response['body']) == len(TEST_PERSON_DATA)


@pytest.mark.asyncio
@pytest.mark.usefixtures("person_to_es")
async def test_list_with_search_wrong_name(make_get_request):
    response = await make_get_request(
        path='persons/search/',
        query_data={'query': 'wrong_name'}
    )
    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.usefixtures("person_to_es")
async def test_person_by_wrong_id(make_get_request):
    response = await make_get_request('persons/any_string')
    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.usefixtures("person_to_es")
async def test_redis_stored_data(make_get_request):
    # Делаем запрос к ES = кэшируем ответ
    await make_get_request(f'persons/{TEST_PERSON_DATA[2]["uuid"]}')
    # Получаем данные из Redis
    response = await make_get_request(path=f'persons/{TEST_PERSON_DATA[2]["uuid"]}')
    assert response['status'] == HTTPStatus.OK
    assert response['body']['full_name'] == TEST_PERSON_DATA[2]['full_name']
    assert response['body']['uuid'] == TEST_PERSON_DATA[2]['uuid']
