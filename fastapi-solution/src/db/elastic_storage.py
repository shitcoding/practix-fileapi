from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError


from .base import Storage
from pydantic import BaseModel

class ElasticStorage(Storage):
    def __init__(
            self,
            model: type[BaseModel],
            index: str,
            elastic_client: AsyncElasticsearch
    ):
        super().__init__(model)
        self.model = model
        self.index = index
        self.es = elastic_client

    def __call__(self):
        return self

    async def get(self, doc_id: str) -> BaseModel | None:
        try:
            response = await self.es.get(index=self.index, id=doc_id)
            return self.model(**response["_source"])
        except NotFoundError:
            return None

    def search(self, query: dict) -> list[BaseModel]:
        pass

    def count(self, query: dict) -> int:
        pass