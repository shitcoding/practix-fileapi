from abc import ABC, abstractmethod


class BaseService(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def save(self, *args, **kwargs):
        pass
