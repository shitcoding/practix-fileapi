import os

import aiofiles
from aiohttp import ClientSession
from core.config import settings
from db.minio import get_minio_client
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from miniopy_async import Minio
from miniopy_async.helpers import ObjectWriteResult
from services.base import BaseService


class MinioService(BaseService):
    def __init__(self, client: Minio):
        self.client = client

    async def save(
        self,
        file: UploadFile,
        path: str,
        bucket_name: str = settings.minio.bucket,
    ) -> ObjectWriteResult:
        """Save a file to minIO storage."""

        exists = await self.client.bucket_exists(bucket_name)
        if not exists:
            await self.client.make_bucket(bucket_name)

        async with aiofiles.tempfile.NamedTemporaryFile(
            delete=False
        ) as temp_file:
            await temp_file.write(await file.read())
            temp_file_path = temp_file.name

        with open(temp_file_path, 'rb') as data:
            result = await self.client.put_object(
                bucket_name=bucket_name,
                object_name=path,
                data=data,
                length=-1,
                part_size=settings.minio.chunk_size
            )

        os.remove(temp_file_path)

        return result

    async def get(
        self,
        path: str,
        bucket_name: str = settings.minio.bucket,
    ) -> StreamingResponse:
        """Get a file from minIO storage as StreamingResponse object."""
        session = ClientSession()
        result = await self.client.get_object(bucket_name, path, session)

        async def s3_stream():
            async for chunk in result.content.iter_chunked(32 * 1024):
                yield chunk

        return StreamingResponse(
            content=s3_stream(),
            headers={
                'Content-Disposition': f'filename="{path.rsplit('/', 1)[-1]}"'
            },
        )


async def get_minio_service() -> MinioService:
    client = await get_minio_client()
    return MinioService(client)
