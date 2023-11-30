import pytest

from tests.functional.settings import get_settings

test_settings = get_settings()


@pytest.mark.asyncio
async def test_search(es_data_loader, make_get_request):
    await es_data_loader()
    query_data = {'query': 'The Star'}
    response = await make_get_request(
        path='films/search',
        query_data=query_data,
    )

    status = response.get('status')
    body = response.get('body')

    assert status == 200
    assert len(body) == 50
