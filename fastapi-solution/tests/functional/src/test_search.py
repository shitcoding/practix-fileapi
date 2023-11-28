import datetime
import uuid

import pytest

from tests.functional.settings import get_settings

test_settings = get_settings()


@pytest.mark.asyncio
async def test_search(es_write_data, make_get_request):
    # 1. Генерируем данные для ES
    es_data = [{
        'uuid': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': ['Action', 'Sci-Fi'],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'name': 'Ann'},
            {'id': 'fb111f22-121e-44a7-b78f-b19191810fbf', 'name': 'Bob'}
        ],
        'writers': [
            {'id': 'caf76c67-c0fe-477e-8766-3ab3ff2574b5', 'name': 'Ben'},
            {'id': 'b45bd7bc-2e16-46d5-b125-983d356768c6', 'name': 'Howard'}
        ],
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat(),
        'film_work_type': 'movie'
    } for _ in range(60)]

    bulk_query: list[dict] = []
    for row in es_data:
        data = {'_index': 'movies', '_id': row['uuid']}
        data.update({'_source': row})
        bulk_query.append(data)

    # 2. Загружаем данные в ES
    await es_write_data(bulk_query)

    # 3. Запрашиваем данные из ES по API
    query_data = {'query': 'The Star'}
    response = await make_get_request(
        path='films/search',
        query_data=query_data,
    )

    # 4. Проверяем ответ
    status = response.get('status')
    body = response.get('body')
    assert status == 200
    assert len(body) == 50
