    
from fastapi import UploadFile
from miniopy_async import Minio
from miniopy_async.helpers import ObjectWriteResult
from aiohttp import ClientSession,tempfile
from starlette.responses import FileResponse,StreamingResponse
from sqlalchemy import Base, Column,String,Integer,DateTime,Index,UUID
import uuid
import datetime
from datetime import timedelta

class FileDbModel(Base):
    __tablename__ = 'files'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path_in_storage = Column(String(255), nullable=False, unique=True)
    filename = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)
    file_type = Column(String(100), nullable=True)
    short_name = Column(String(24), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    Index('idx_file_path', 'path_in_storage')
    Index('idx_file_short_name', 'short_name')

    def __init__(self, path_in_storage: str, filename: str, short_name: str, size: int, file_type: str) -> None:
        self.path_in_storage = path_in_storage
        self.filename = filename
        self.short_name = short_name
        self.size = size
        self.file_type = file_type

    def __repr__(self) -> str:
        return f'<id {self.id}>'

class MinioStorage:
    def __init__(self):
        # код упрощен для демонстрации, правильнее инициализировать соединение один раз 
        # и внедрять в сервис в качестве зависимости
        self.client = Minio(
            endpoint='minio_service:9000', 
            access_key='AKIAVMFI4QKHTS6RSWFE', 
            secret_key='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', 
            secure=False,
        )

    async def save(self, file: UploadFile, bucket: str, path: str) -> ObjectWriteResult:
        result = await self.client.put_object(
            bucket_name=bucket, object_name=path, data=file, length=-1, part_size=10 * 1024 * 1024,
        )
        return result

    async def get_file(self, bucket: str, path: str) -> StreamingResponse:
        session = ClientSession()
        result = await self.client.get_object(bucket, path, session)
        
        async def s3_stream():
            async for chunk in result.content.iter_chunked(32 * 1024):
                yield chunk

        return StreamingResponse(
            content=s3_stream(),
            media_type='video/mp4',
            headers={'Content-Disposition': 'filename="movie.mp4"'}
        )
    
    async def get_presigned_url(self, bucket: str, path: str) -> str:
        return await self.client.get_presigned_url('GET', bucket, path, expires=timedelta(days=1),)