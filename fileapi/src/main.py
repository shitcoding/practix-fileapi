import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.files import router as files_router
from core.config import settings
from core.logger import LOGGING
from db.postgres import init_db


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

app.include_router(
    files_router, prefix='/fileapi/api/v1/files', tags=['files']
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.app_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=settings.debug,
    )
