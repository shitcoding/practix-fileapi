import logging

from elasticsearch import AsyncElasticsearch, NotFoundError
from .base import Storage
from pydantic import BaseModel


class ElasticStorage(Storage):
    def __init__(
            self,
            elastic_client: AsyncElasticsearch
    ):
        self.model = None
        self.index = None
        self.es = elastic_client

    def init(
            self,
            model: type[BaseModel],
            index: str
    ) -> "ElasticStorage":
        self.model = model
        self.index = index
        return self

    def __call__(self):
        return self

    def __deepcopy__(self, memodict=None):
        return type(self)(self.es)

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
                body=query
            )
            return [hit["_source"] for hit in response["hits"]["hits"]]
        except Exception as e:
            logging.error(e)
            return []
