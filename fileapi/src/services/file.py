import os
from datetime import datetime
from functools import lru_cache

import shortuuid
from fastapi import Depends, UploadFile
from fastapi.responses import StreamingResponse

from core.config import settings
from db.postgres import get_session
from models.file_properties import FilePropertiesCreate
from services.base import BaseService
from services.file_properties import (FilePropertiesService,
                                      get_file_properties_service)
from services.minio import MinioService, get_minio_service


class FileService(BaseService):
    def __init__(
        self,
        file_properties_service: FilePropertiesService,
        minio_service: MinioService,
    ):
        self.file_properties_service = file_properties_service
        self.minio_service = minio_service

    async def _get_file_properties(self, file: UploadFile) -> FilePropertiesCreate:
        file_size = os.fstat(file.file.fileno()).st_size
        file_name = file.filename
        file_type = file.content_type
        short_name = shortuuid.ShortUUID().random(length=24)

        path_in_storage = f'films/{file_name}'   # TODO: move prefix to config

        return FilePropertiesCreate(
            path_in_storage=path_in_storage,
            filename=file_name,
            size=file_size,
            file_type=file_type, # TODO: Fix detection of file_type (currently is None)
            short_name=short_name,
            created_at=datetime.utcnow(),
        )

    async def get(self, short_name: str) -> StreamingResponse:
        file_properties = await self.file_properties_service.get(short_name)
        if not file_properties:
            return {'error': 'File not found'}
        return await self.minio_service.get(file_properties.path_in_storage)

    async def save(self, file: UploadFile):
        file_properties = await self._get_file_properties(file)
        # Save the file to MinIO
        await self.minio_service.save(file, file_properties.path_in_storage)
        # Save file properties to the database
        db_file_properties = await self.file_properties_service.save(
            file_properties
        )
        return {
            'message': 'File uploaded successfully',
            'file_properties': db_file_properties,
        }


@lru_cache
def get_file_service(
    file_properties_service: FilePropertiesService = Depends(
        get_file_properties_service
    ),
    minio_service: MinioService = Depends(get_minio_service),
) -> FileService:
    return FileService(file_properties_service, minio_service)
