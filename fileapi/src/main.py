import logging

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import ORJSONResponse

from core.config import settings
from core.logger import LOGGING
from db.minio import MinioStorage

from api.v1.films import router as router

app = FastAPI(
    title=settings.project_name,
    docs_url='/fileapi/openapi',
    openapi_url='/fileapi/openapi.json',
    default_response_class=ORJSONResponse,
)


app.include_router(router, prefix='/fileapi/v1/files', tags=['files'])

minio_storage = MinioStorage()


@app.get('/fileapi/')
async def hello():
    return {'Hello': 'FileAPI'}


@app.post('/fileapi/upload/')
async def upload_file(file: UploadFile = File(...)):
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
async def get_file(s3_path: str):
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
        reload=True,
    )
