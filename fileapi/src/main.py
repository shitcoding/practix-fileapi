import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings
from core.logger import LOGGING

app = FastAPI(
    title=settings.project_name,
    default_response_class=ORJSONResponse,
)


@app.get('/fileapi/')
async def hello():
    return {'Hello': 'FileAPI'}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.app_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
