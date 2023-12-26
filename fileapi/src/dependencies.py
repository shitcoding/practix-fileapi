from fastapi import Depends

from db.minio import get_minio_client
from db.postgres import get_session
from services.base import BaseService
from services.file_properties import FilePropertiesService
from services.minio import MinioService


async def get_file_props_service(db_session=Depends(get_session)) -> BaseService:
    yield FilePropertiesService(db_session)


async def get_s3_service(s3_client=Depends(get_minio_client)) -> BaseService:
    client = MinioService(s3_client)
    try:
        yield client
    finally:
        await client.close()
