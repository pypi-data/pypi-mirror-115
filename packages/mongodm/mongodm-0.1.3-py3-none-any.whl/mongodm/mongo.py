from typing import Any, Union

import pymongo
from pymongo.collection import Collection as PymongoCollection
from pymongo.cursor import Cursor
from pymongo.database import Database as PymongoDatabase

from .query import Q


class MongoClient(pymongo.MongoClient):
    def __call__(self, database: str):
        return self.__getattr__(database)

    def __getitem__(self, database: str) -> "Database":
        return Database(self, database)


class Database(PymongoDatabase):
    def __call__(self, collection: str):
        return self.__getattr__(collection)

    def __getitem__(self, collection: str) -> "Collection":
        return Collection(self, collection)


class Collection(PymongoCollection):
    def find(
        self,
        query: Union[Q, dict],
        limit: int = 0,
        skip: int = 0,
        sort: Any = None,
        *args: Any,
        **kwargs: Any
    ):
        return Cursor(
            self, filter=query, limit=limit, skip=skip, sort=sort, *args, **kwargs
        )
