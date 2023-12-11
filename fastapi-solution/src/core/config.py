import os
from logging import config as logging_config

import functools

from pydantic import Field
from pydantic_settings import BaseSettings

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class ProjectSettings(BaseSettings):
    project_name: str = Field('movies', env='PROJECT_NAME')
    base_dir: str = Field(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FastAPISettings(BaseSettings):
    default_page_size: int = Field(10)

    class Config:
        ignored_types = (functools.cached_property,)


class ElasticsearchSettings(BaseSettings):
    es_scheme: str = Field('http', env='ES_SCHEME')
    es_host: str = Field('127.0.0.1', env='ES_HOST')
    es_port: int = Field(9200, env='ES_PORT')
    es_movies_index: str = Field('movies', env='ES_MOVIES_INDEX')
    es_genres_index: str = Field('genres', env='ES_GENRES_INDEX')
    es_persons_index: str = Field('persons', env='ES_PERSONS_INDEX')

    class Config:
        ignored_types = (functools.cached_property,)


class RedisSettings(BaseSettings):
    redis_host: str = Field('127.0.0.1', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')
    redis_expire: int = Field(60 * 5)

    class Config:
        ignored_types = (functools.cached_property,)


class Settings(BaseSettings):
    project: ProjectSettings = ProjectSettings()
    fastapi: FastAPISettings = FastAPISettings()
    elastic: ElasticsearchSettings = ElasticsearchSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
