import uvicorn
from api.v1.films import router as f_router
from api.v1.genres import router as g_router
from api.v1.persons import router as p_router
from core import config
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(f_router, prefix='/api/v1/films', tags=['films'])
app.include_router(g_router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(p_router, prefix='/api/v1/persons', tags=['persons'])

if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', port=5000, log_level="info")
