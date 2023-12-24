from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import StreamingResponse

from services.file import FileService, get_file_service

router = APIRouter()


@router.post('/upload/')
async def upload_file(
    file: UploadFile = File(...),
    file_service: FileService = Depends(get_file_service),
):
    return await file_service.save(file)


@router.get('/get/{short_name}')
async def get_file(
    short_name: str,
    file_service: FileService = Depends(get_file_service),
) -> StreamingResponse:
    return await file_service.get(short_name)
