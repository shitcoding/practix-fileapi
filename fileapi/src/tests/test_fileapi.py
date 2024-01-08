import uuid
from datetime import datetime
from io import BytesIO

import pytest
from fastapi.responses import StreamingResponse

from models.file_properties import FilePropertiesRead
from services.file import FileServiceABC
from http import HTTPStatus


@pytest.mark.asyncio
async def test_upload_file(async_client, mocker, app_fixture):
    mock_file_service = mocker.MagicMock(spec=FileServiceABC)
    mock_file_service.save.return_value = {
        'message': 'File uploaded successfully'
    }
    app_fixture.dependency_overrides[
        FileServiceABC
    ] = lambda: mock_file_service

    data = {'file': ('testfile.txt', BytesIO(b'test data'), 'text/plain')}
    response = await async_client.post(
        '/fileapi/api/v1/files/upload/', files=data
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'File uploaded successfully'}


@pytest.mark.asyncio
async def test_get_file(async_client, mocker, app_fixture):
    async def content_generator():
        yield b'test data'

    mock_file_service = mocker.MagicMock(spec=FileServiceABC)
    mock_file_service.get.return_value = StreamingResponse(
        content=content_generator()
    )
    app_fixture.dependency_overrides[
        FileServiceABC
    ] = lambda: mock_file_service

    response = await async_client.get(
        '/fileapi/api/v1/files/download-stream/testfile'
    )

    assert response.status_code == HTTPStatus.OK
    assert await response.aread() == b'test data'


@pytest.mark.asyncio
async def test_get_file_info(async_client, mocker, app_fixture):
    mock_file_service = mocker.MagicMock(spec=FileServiceABC)
    file_properties = FilePropertiesRead(
        id=uuid.uuid4(),
        path_in_storage='path/to/storage',
        filename='testfile.txt',
        size=123,
        file_type='text/plain',
        short_name='shortname',
        created_at=datetime.utcnow(),
    )
    mock_file_service.get_info.return_value = file_properties
    app_fixture.dependency_overrides[
        FileServiceABC
    ] = lambda: mock_file_service

    response = await async_client.get(
        '/fileapi/api/v1/files/get_info/testfile'
    )

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
