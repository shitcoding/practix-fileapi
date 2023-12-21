import logging

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import ORJSONResponse

from core.config import settings
from core.logger import LOGGING
from db.minio import MinioStorage

app = FastAPI(
    title=settings.project_name,
    docs_url='/fileapi/openapi',
    openapi_url='/fileapi/openapi.json',
    default_response_class=ORJSONResponse,
)

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


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.app_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
