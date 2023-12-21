import os

import aiofiles
from fastapi import UploadFile
from miniopy_async import Minio
from miniopy_async.helpers import ObjectWriteResult

from core.config import settings


class MinioStorage:
    def __init__(self):
        # TODO: код упрощен для демонстрации, правильнее инициализировать соединение один раз
        # и внедрять в сервис в качестве зависимости
        self.client = Minio(
            endpoint=settings.minio.endpoint,
            access_key=settings.minio.access_key,
            secret_key=settings.minio.secret_key,
            secure=settings.minio.secure,
        )

    async def save(
        self,
        file: UploadFile,
        path: str,
        bucket_name: str = settings.minio.bucket,
    ) -> ObjectWriteResult:

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
                part_size=10
                * 1024
                * 1024,  # TODO: move chunk size to settings
            )

        os.remove(temp_file_path)

        return result
