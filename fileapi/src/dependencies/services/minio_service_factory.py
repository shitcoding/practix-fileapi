from functools import cache

from fastapi import Depends

from db.minio import get_minio_client
from dependencies.registrator import add_factory_to_mapper
from services.s3 import MinioService, S3ServiceABC


@add_factory_to_mapper(S3ServiceABC)
@cache
def create_minio_service(
    s3_client=Depends(get_minio_client),
) -> MinioService:
    return MinioService(s3_client)
