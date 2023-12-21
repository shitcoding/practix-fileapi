from logging import config as logging_config
from pathlib import Path

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING

# Настройки логгера
logging_config.dictConfig(LOGGING)

# Корень проекта fileapi
BASE_DIR = Path(__file__).parent.parent.parent


class DataBaseSettings(BaseSettings):
    # Настройки Postgres БД FileAPI сервиса
    user: str = ...
    password: str = ...
    db: str = ...
    host: str = ...
    port: int = ...

    model_config = SettingsConfigDict(
        env_prefix='postgres_',
        env_file=BASE_DIR / 'api.env',
        extra='ignore',
    )

    @property
    def url(self):
        return f'postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'


class MinIOSettings(BaseSettings):
    host: str = 'minio'
    port: str = 9000
    access_key: str = ...
    secret_key: str = ...
    bucket: str = 'files-storage'
    secure: bool = False

    model_config = SettingsConfigDict(
        env_prefix='minio_',
        env_file=BASE_DIR / 'api.env',
        extra='ignore',
    )

    @property
    def endpoint(self):
        return f'{self.host}:{self.port}'


class FileAPISettings(BaseSettings):
    # Настройки FileAPI сервиса
    project_name: str = 'FileAPI'   # Используется в Swagger-документации
    project_description: str = 'MinIO S3 file storage API service'

    app_port: int = 8000

    db: DataBaseSettings = DataBaseSettings()
    minio: MinIOSettings = MinIOSettings()

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / 'api.env',
        extra='ignore',
    )


settings = FileAPISettings()
