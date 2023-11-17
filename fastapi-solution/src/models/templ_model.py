import orjson

from pydantic import BaseModel, Field, UUID4


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class IdMix(BaseModel):
    id: str

    class Config:
        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps