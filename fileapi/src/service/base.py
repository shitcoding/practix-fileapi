from abc import ABC, abstractmethod

from psycopg2.extensions import connection

from fileapi.src.db.minio import MinioStorage


class Service(ABC):
    @abstractmethod
    def __init__(self, db: connection, #Здесь нужно storage с БД
                 s3_client: MinioStorage):
        self.db = db
        self.s3_client = s3_client

    @abstractmethod
    def get(self, file_id: str):
        pass

    @abstractmethod
    def save(self, file: object):
        pass