import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title='FileAPI',
    default_response_class=ORJSONResponse,
)

@app.get('/')
async def hello():
    return {'Hello': 'FileAPI'} 

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
