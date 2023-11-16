import logging
from typing import Optional

import elasticsearch
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Search
from fastapi import HTTPException, status
from pydantic import BaseModel

from .base import Storage


class ElasticStorage(Storage):
    def __init__(self, model: type[BaseModel], index: str, elastic: AsyncElasticsearch):
        super().__init__(model)
        self.model = model
        self.index = index
        self.client = elastic

    def __call__(self):
        return self

    async def get(self, doc_id: str) -> BaseModel | None:
        try:
            response = await self.client.get(index=self.index, id=doc_id)

            return self.model(**response["_source"])
        except NotFoundError:
            return None

    async def search(self, query: dict) -> list[BaseModel]:
        try:
            result = await self.client.search(index=self.index, body=query)
        except elasticsearch.exceptions.RequestError as re:
            print(re)
            if re.error == "search_phase_execution_exception":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")
            raise re

        if not result["hits"]["total"]["value"]:
            return []
        items = [self.model(**hit["_source"]) for hit in result["hits"]["hits"]]
        return items

    def count(self, query: dict) -> int:
        pass