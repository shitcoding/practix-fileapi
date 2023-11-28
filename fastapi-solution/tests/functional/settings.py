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
    es_index: str = Field(..., env='ES_INDEX')
    es_index_mapping: dict = Field({
        "mappings": {
            "properties": {
                "uuid": {
                    "type": "keyword"
                },
                "imdb_rating": {
                    "type": "float"
                },
                "genre": {
                    "type": "keyword"
                },
                "title": {
                    "type": "text"
                },
                "description": {
                    "type": "text"
                },
                "director": {
                    "type": "keyword"
                },
                "actors_names": {
                    "type": "keyword"
                },
                "writers_names": {
                    "type": "keyword"
                },
                "actors": {
                    "type": "nested",
                    "properties": {
                        "id": {
                            "type": "keyword"
                        },
                        "name": {
                            "type": "keyword"
                        }
                    }
                },
                "writers": {
                    "type": "nested",
                    "properties": {
                        "id": {
                            "type": "keyword"
                        },
                        "name": {
                            "type": "keyword"
                        }
                    }
                },
                "created_at": {
                    "type": "date"
                },
                "updated_at": {
                    "type": "date"
                },
                "film_work_type": {
                    "type": "keyword"
                }
            }
        }
    }, env='ES_INDEX_MAPPING')

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
