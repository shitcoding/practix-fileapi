from logging import config as logging_config
from pathlib import Path

from core.logger import LOGGING
from pydantic_settings import BaseSettings, SettingsConfigDict

# Logger config
logging_config.dictConfig(LOGGING)

# Base dir of fileapi service
BASE_DIR = Path(__file__).parent.parent.parent


class DataBaseSettings(BaseSettings):
    user: str = ...
    password: str = ...
    db: str = ...
    host: str = ...
    port: int = ...

    content_prefix: str = 'films/'

    model_config = SettingsConfigDict(
        env_prefix='postgres_',
        env_file=BASE_DIR / 'api.env',
        extra='ignore',
    )

    @property
    def url(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'


class MinIOSettings(BaseSettings):
    host: str = 'minio'
    port: str = 9000
    access_key: str = ...
    secret_key: str = ...
    bucket: str = 'files-storage'
    secure: bool = False
    chunk_size: int = 10 * 1024 * 1024

    model_config = SettingsConfigDict(
        env_prefix='minio_',
        env_file=BASE_DIR / 'api.env',
        extra='ignore',
    )

    @property
    def endpoint(self):
        return f'{self.host}:{self.port}'


class FileAPISettings(BaseSettings):
    project_name: str = 'FileAPI'   # Used in Swagger docs
    project_description: str = 'MinIO S3 file storage API service'

    app_port: int = 8000
    debug: bool = False

    db: DataBaseSettings = DataBaseSettings()
    minio: MinIOSettings = MinIOSettings()

    model_config = SettingsConfigDict(
        env_prefix='fileapi_',
        env_file=BASE_DIR / 'api.env',
        extra='ignore',
    )


settings = FileAPISettings()
