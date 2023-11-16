import abc

from pydantic import BaseModel as Base
from typing_extensions import TypeVar

BaseModel = TypeVar("BaseModel", bound=Base)

class Cache(abc.ABC):
    def __call__(self):
        return self

    async def get(self, key: str) -> BaseModel | None:
        pass

    async def set(self, key: str, value: BaseModel, expire: int):
        pass

    async def get_list(self, key: str) -> list[BaseModel]:
        pass

    async def set_list(self, key: str, value: list[BaseModel], expire: int):
        pass


class Storage(abc.ABC):
    def __init__(self, model: type[BaseModel]):
        self.model = model

    def __call__(self):
        return self

    async def get(self, doc_id: str) -> BaseModel | None:
        pass

    async def search(self, query: dict) -> list[BaseModel]:
        pass

    async def count(self, query: dict) -> int:
        pass