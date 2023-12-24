import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.responses import ORJSONResponse, StreamingResponse

from core.config import settings
from core.logger import LOGGING
from db.postgres import init_db
from services.file import FileService, get_file_service


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Create database tables
    await init_db()

    yield


app = FastAPI(
    title=settings.project_name,
    description=settings.project_description,
    docs_url='/fileapi/openapi',
    openapi_url='/fileapi/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


@app.post('/fileapi/upload/')
async def upload_file(
    file: UploadFile = File(...),
    file_service: FileService = Depends(get_file_service),
):
    return await file_service.save(file)


@app.get('/fileapi/get/{short_name}') # TODO: Maybe change short_name to id
async def get_file(
    short_name: str,
    file_service: FileService = Depends(get_file_service),
) -> StreamingResponse:
    return await file_service.get(short_name)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.app_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=settings.debug,
    )
