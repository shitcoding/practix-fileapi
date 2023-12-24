from fastapi import APIRouter, File, UploadFile, Depends

from fileapi.src.db.minio import MinioStorage
from fileapi.src.service.file import get_file_service, FileService

router = APIRouter()

minio_storage = MinioStorage()


@router.post('/upload')
async def upload_file(file: UploadFile = File(...), file_service: FileService = Depends(get_file_service)):
    try:
        # Use the original filename or generate a new name
        file_name = file.filename
        # Save the file to MinIO
        result = await file_service.save(file=file)
        return {
            'message': 'File uploaded successfully',
            'result': str(result),
        }
    except Exception as e:
        return {'error': str(e)}


@router.get('/get/{s3_path}')
async def get_file(s3_path: str):
    try:
        streaming_response = await minio_storage.get(s3_path)
        return streaming_response
    except Exception as e:
        return {'error': str(e)}
