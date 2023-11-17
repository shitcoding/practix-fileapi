import logging

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

    async def search(
            self,
            query: dict[str, any],
            size: int = 10,
            from_: int = 0,
    ) -> list[dict[str, any]]:
        try:
            response = await self.es.search(
                index=self.index,
                body=query,
                size=size,
                from_=from_
            )
            return [hit["_source"] for hit in response["hits"]["hits"]]
        except Exception as e:
            logging.error(e)
            return []

    def count(self, query: dict) -> int:
        pass
