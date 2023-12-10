import functools

from pydantic import Field
from pydantic_settings import BaseSettings


class FastAPISettings(BaseSettings):
    app_host: str = Field(..., env='APP_HOST')
    app_port: int = Field(..., env='APP_PORT')

    class Config:
        ignored_types = (functools.cached_property,)


class ElasticsearchSettings(BaseSettings):
    es_host: str = Field(..., env='ES_HOST')
    es_port: int = Field(..., env='ES_PORT')
    es_movies_index: str = Field(..., env='ES_MOVIES_INDEX')
    es_genres_index: str = Field(..., env='ES_GENRES_INDEX')
    es_persons_index: str = Field(..., env='ES_PERSONS_INDEX')

    class Config:
        ignored_types = (functools.cached_property,)


class RedisSettings(BaseSettings):
    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')

    class Config:
        ignored_types = (functools.cached_property,)


class Settings(BaseSettings):
    fastapi: FastAPISettings = FastAPISettings()
    elastic: ElasticsearchSettings = ElasticsearchSettings()
    redis: RedisSettings = RedisSettings()


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()
