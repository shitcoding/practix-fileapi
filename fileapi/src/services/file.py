import os
from datetime import datetime
from functools import lru_cache

import shortuuid
from fastapi import Depends, UploadFile
from fastapi.responses import StreamingResponse

from models.file_properties import FilePropertiesCreate

from dependencies import get_file_props_service, get_s3_service
from models.file_properties import FilePropertiesUpdate
from services.base import BaseService


class FileService(BaseService):
    def __init__(
        self,
        file_properties_service: BaseService,
        s3_service: BaseService,
    ):
        self.file_properties_service = file_properties_service
        self.s3_service = s3_service

    async def _get_file_properties(self, file: UploadFile) -> FilePropertiesCreate:
        file_size = os.fstat(file.file.fileno()).st_size
        file_name = file.filename
        file_type = file.content_type
        short_name = shortuuid.ShortUUID().random(length=24)

        path_in_storage = f'{settings.db.content_prefix}{file_name}'

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
        return await self.s3_service.get(file_properties.path_in_storage)

    async def get_info(self, short_name: str) -> StreamingResponse:
        file_properties = await self.file_properties_service.get(short_name)
        if not file_properties:
            return {'error': 'File not found'}
        return file_properties

    async def save(self, file: UploadFile):
        file_properties = await self._get_file_properties(file)
        # Save the file to MinIO
        await self.s3_service.save(file, file_properties.path_in_storage)
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
    file_properties_service: BaseService = Depends(get_file_props_service),
    s3_service: BaseService = Depends(get_s3_service),
) -> FileService:
    return FileService(file_properties_service, s3_service)
