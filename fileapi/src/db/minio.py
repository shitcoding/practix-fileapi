from core.config import settings
from miniopy_async import Minio


async def get_minio_client() -> Minio:
    """Create Minio client."""
    minio_client = Minio(
        endpoint=settings.minio.endpoint,
        access_key=settings.minio.access_key,
        secret_key=settings.minio.secret_key,
        secure=settings.minio.secure,
    )
    return minio_client
