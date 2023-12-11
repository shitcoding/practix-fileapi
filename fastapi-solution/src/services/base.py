from db.base import Cache, Storage
from abc import ABC, abstractmethod


class Service(ABC):
    @abstractmethod
    def __init__(self, cache: Cache, storage: Storage):
        self.cache = cache
        self.storage = storage

    @abstractmethod
    def get_by_id(self, genre_id: str):
        pass


class ExtService(Service):
    @abstractmethod
    def search(self, query: str, sort: str, page: int, size: int):
        pass

    @staticmethod
    def _build_search_query(query: str, sort: str, page: int, size: int):
        pass
