from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import StreamingResponse

from models.file_properties import FilePropertiesRead
from services.file import FileServiceABC

router = APIRouter()


@router.post(
    '/upload/',
    summary='Upload file',
    description="Endpoint that uploads file to S3 storage and saves its' properties to database",
)
async def upload_file(
    file: UploadFile = File(...),
    file_service: FileServiceABC = Depends(),
):
    return await file_service.save(file)


@router.get(
    '/download-stream/{short_name}',
    summary='Get file',
    description='Get file from S3 storage as StreamingResponse by short_name',
)
async def get_file(
    short_name: str,
    file_service: FileServiceABC = Depends(),
) -> StreamingResponse:
    return await file_service.get(short_name)


@router.get(
    '/get_info/{short_name}',
    summary='Get file info',
    description='Get file properties by short_name of the file',
)
async def get_file_info(
    short_name: str,
    file_service: FileServiceABC = Depends(),
) -> FilePropertiesRead:
    return await file_service.get_info(short_name)
