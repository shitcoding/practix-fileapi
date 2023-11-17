import abc
from pydantic import BaseModel


class Cache(abc.ABC):
    def __call__(self):
        return self

    async def get(self, key: str) -> BaseModel | None:
        pass

    async def set(self, key: str, value: BaseModel, expire: int):
        pass


class Storage(abc.ABC):
    def __init__(self, model: type[BaseModel]):
        self.model = model

    def __call__(self):
        return self

    def get(self, doc_id: str) -> BaseModel | None:
        pass

    async def search(self, query: dict[str, any]) -> list[dict[str, any]]:
        pass

    def count(self, query: dict) -> int:
        pass