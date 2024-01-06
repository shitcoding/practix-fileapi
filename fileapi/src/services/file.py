import os
from abc import ABC, abstractmethod
from datetime import datetime
from http import HTTPStatus

import shortuuid
from fastapi import HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from core.config import settings
from models.file_properties import FilePropertiesCreate, FilePropertiesRead
from services.file_properties import FilePropertiesServiceABC
from services.s3 import S3ServiceABC


class FileServiceABC(ABC):
    """Abstract base class for uploading/getting the files."""

    @abstractmethod
    async def get(self, short_name: str) -> StreamingResponse | HTTPException:
        ...

    @abstractmethod
    async def get_info(
        self, short_name: str
    ) -> FilePropertiesRead | HTTPException:
        ...

    @abstractmethod
    async def save(self, file: UploadFile) -> dict:
        ...


class FileService(FileServiceABC):
    """File service implementation based on Postgres and Minio services."""

    def __init__(
        self,
        file_properties_service: FilePropertiesServiceABC,
        s3_service: S3ServiceABC,
    ):
        self.file_properties_service = file_properties_service
        self.s3_service = s3_service

    @staticmethod
    async def _get_file_properties(file: UploadFile) -> FilePropertiesCreate:
        file_size = os.fstat(file.file.fileno()).st_size
        file_name = file.filename
        file_type = file.content_type
        short_name = shortuuid.ShortUUID().random(length=24)

        path_in_storage = f'{settings.db.content_prefix}{file_name}'

        return FilePropertiesCreate(
            path_in_storage=path_in_storage,
            filename=file_name,
            size=file_size,
            file_type=file_type,
            short_name=short_name,
            created_at=datetime.utcnow(),
        )

    async def get(self, short_name: str) -> StreamingResponse | HTTPException:
        file_properties = await self.file_properties_service.get(short_name)
        if not file_properties:
            return HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='File not found'
            )
        return await self.s3_service.get(file_properties.path_in_storage)

    async def get_info(
        self, short_name: str
    ) -> FilePropertiesRead | HTTPException:
        file_properties = await self.file_properties_service.get(short_name)
        if not file_properties:
            return HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='File not found'
            )
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
