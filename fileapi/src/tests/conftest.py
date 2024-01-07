import pytest_asyncio
from httpx import AsyncClient

from main import app


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest_asyncio.fixture
def app_fixture():
    return app
