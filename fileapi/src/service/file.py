from typing import Optional

from fastapi import HTTPException

from fileapi.src.service.base import Service
from fileapi.src.models.file import FileDbModel

from fileapi.src.core.config import settings


class FileService(Service):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def get(self, file_id: str) -> Optional[dict]:
        meta_data = await self.db.get(id=file_id) #draft зависит от определения DB
        # Ожидается структура типа FileDbModel
        if meta_data:
            streaming_response = await self.s3_client.get(path=meta_data.path_in_storage)
            return {"file_meta": meta_data, "streaming_response": streaming_response}
        else:
            raise HTTPException(status_code=404, detail=f"File {file_id} not found")

    async def save(self, file: FileDbModel) -> FileDbModel:
        await self.db.put(file) #draft зависит от определения DB
        await self.s3_client.save(file=file, path=file.path_in_storage)
        return file

def get_file_service(
        db : DBSTORAGE,
        s3_client: MinioStorage
) -> FileService:
    return FileService(db, s3_client)

