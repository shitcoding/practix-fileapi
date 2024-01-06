from functools import cache

from fastapi import Depends

from dependencies.registrator import add_factory_to_mapper
from dependencies.services.file_properties_service_factory import \
    create_file_properties_service
from dependencies.services.minio_service_factory import create_minio_service
from services.file import FileService, FileServiceABC
from services.file_properties import FilePropertiesServiceABC
from services.s3 import S3ServiceABC


@add_factory_to_mapper(FileServiceABC)
@cache
def create_file_service(
    file_properties_service: FilePropertiesServiceABC = Depends(
        create_file_properties_service
    ),
    s3_service: S3ServiceABC = Depends(create_minio_service),
) -> FileService:
    return FileService(file_properties_service, s3_service)
