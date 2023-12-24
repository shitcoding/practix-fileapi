import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.responses import ORJSONResponse
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import settings
from core.logger import LOGGING
from db.minio import get_minio_storage
from db.postgres import get_session, init_db
from models.file_properties import (FileProperties, FilePropertiesCreate,
                                    FilePropertiesRead)
from services.minio import MinioStorage


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


@app.post('/fileapi/add-db-file/', response_model=FilePropertiesRead)
async def add_file_properties(
    file_properties: FilePropertiesCreate,
    session: AsyncSession = Depends(get_session),
):
    db_file_properties = FileProperties.model_validate(file_properties)
    session.add(db_file_properties)
    await session.commit()
    await session.refresh(db_file_properties)
    return db_file_properties


@app.get('/fileapi/get-db-files', response_model=list[FilePropertiesRead])
async def get_file_properties_list(
    session: AsyncSession = Depends(get_session),
):
    result = await session.exec(select(FileProperties))
    files_list = result.all()
    return files_list


@app.post('/fileapi/upload/')
async def upload_file(
    file: UploadFile = File(...),
    minio_storage: MinioStorage = Depends(get_minio_storage),
):
    try:
        # Use the original filename or generate a new name
        file_name = file.filename
        # Save the file to MinIO
        result = await minio_storage.save(file, file_name)
        return {
            'message': 'File uploaded successfully',
            'result': str(result),
        }
    except Exception as e:
        return {'error': str(e)}


@app.get('/fileapi/get/{s3_path}')
async def get_file(
    s3_path: str,
    minio_storage: MinioStorage = Depends(get_minio_storage),
):
    try:
        streaming_response = await minio_storage.get(s3_path)
        return streaming_response
    except Exception as e:
        return {'error': str(e)}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.app_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=settings.debug,
    )
