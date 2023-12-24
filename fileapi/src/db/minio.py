from miniopy_async import Minio

from core.config import settings
from services.minio import MinioStorage

minio_client: Minio | None = None


async def get_minio() -> Minio:
    """Create Minio client."""
    minio_client = Minio(
        endpoint=settings.minio.endpoint,
        access_key=settings.minio.access_key,
        secret_key=settings.minio.secret_key,
        secure=settings.minio.secure,
    )
    return minio_client


async def get_minio_storage() -> MinioStorage:
    """Create MinioStorage instance."""
    client = await get_minio()
    minio_storage = MinioStorage(client)
    yield minio_storage
