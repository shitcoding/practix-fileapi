from abc import ABC, abstractmethod
from pydantic import BaseModel as Base
from typing_extensions import TypeVar

BaseModel = TypeVar("BaseModel", bound=Base)


class Cache(ABC):
    def __call__(self):
        return self

    @abstractmethod
    def init(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get(self, key: str) -> str | None:
        pass

    @abstractmethod
    async def set(self, key: str, value: BaseModel, expire: int):
        pass

    @abstractmethod
    async def get_list(self, key: str) -> list[BaseModel]:
        pass

    @abstractmethod
    async def set_list(self, key: str, value: list[BaseModel], expire: int):
        pass


class Storage(ABC):
    @abstractmethod
    def init(self, *args, **kwargs):
        pass

    @abstractmethod
    def __call__(self):
        pass

    @abstractmethod
    async def get(self, *args, **kwargs):
        pass

    @abstractmethod
    async def search(self, *args, **kwargs):
        pass
