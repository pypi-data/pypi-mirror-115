from typing import Any, Callable, Union

from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo.results import DeleteResult

from mongodm.utils import processing_kwargs

from .mongo import Collection, Database


class Id(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: ObjectId) -> ObjectId:
        return value


class Document(BaseModel):
    __collection: Collection

    id: Id = Field(..., alias="_id")

    @classmethod
    @property
    def __collection_name(cls) -> str:
        """Returns class name in camel case if Meta has no attribute
        collection_name or collection_name_generator.

        Returns:
            str: Class name
        """
        try:
            if hasattr(cls, "collection_name"):
                return cls.Meta.collection_name
            elif hasattr(cls, "collection_name_generator"):
                return cls.Meta.collection_name_generator(cls)
            raise AttributeError
        except AttributeError:
            name = cls.__name__
            return name[0].lower() + name[1:]

    @classmethod
    @property
    def collection(cls) -> Collection:
        """Returns a collection by class name

        Returns:
            Collection: Class collection
        """
        try:
            return cls.__collection
        except AttributeError:
            cls.__collection = cls.Meta.database(cls.__collection_name)
            return cls.__collection

    @classmethod
    @processing_kwargs
    def filter(cls, *args: Any, **kwargs: Any) -> list["Document"]:
        """Get one or more documents from database.

        Works like `find` in pymongo.

        MongODM `filter` example:
        >>> Document.filter(hello="world")

        Pymongo `find` example:
        >>> db.test.find({"hello": "world"})

        Returns:
            list[`Document`]: Returns a `list` of documents, or empty `list`
            if no matching document is found.
        """
        return [cls(**data) for data in cls.collection.find(kwargs)]

    @classmethod
    @processing_kwargs
    def get(cls, *args: Any, **kwargs: Any) -> Union["Document", None]:
        """Get a single document from the database.

        Works like `find_one` in pymongo.

        MongODM `filter` example:
        >>> Document.get(hello="world")

        Pymongo `find` example:
        >>> db.test.find_one({"hello": "world"})

        Returns:
            Union[`Document`, `None`]: Returns a single document, or `None` if no matching
            document is found.
        """
        obj = cls.collection.find_one(kwargs)
        return cls(**obj) if obj is not None else None

    @classmethod
    def create(cls, *args: Any, **kwargs: Any) -> "Document":
        """Create document in the class collection.

        Returns:
            `Document`: Document model with `ObjectID` and included fields.
        """
        obj = cls.collection.insert_one(kwargs).inserted_id
        return cls(id=obj, **kwargs)

    @classmethod
    def create_many(
        cls, *data: dict[str, Any], in_model=False, **kwargs
    ) -> list[Union[ObjectId, "Document"]]:
        """Create multiple documents in the class collection.

        Returns:
            list[Union[`ObjectId`, `Document`]]: Returns `list` with `ObjectId`
            only if `in_model` is `False`, else returns `list` with `Document` model
        """
        object_ids = cls.collection.insert_many(data).inserted_ids
        if not in_model:
            return object_ids
        return [cls(id=_id, **values) for _id, values in zip(object_ids, data)]

    @classmethod
    @processing_kwargs
    def delete_one(cls, *args: Any, **kwargs: Any) -> DeleteResult:
        """Delete document in the class collection.

        Returns:
            DeleteResult: Delete result from Pymongo.
        """
        return cls.collection.delete_one(kwargs)

    @classmethod
    @processing_kwargs
    def delete_many(cls, *args: Any, **kwargs: Any) -> DeleteResult:
        """Delete multiple documents in the class collection.

        Returns:
            DeleteResult: Delete result from Pymongo.
        """
        return cls.collection.delete_many(kwargs)

    def delete(self) -> DeleteResult:
        """Delete instance.

        Returns:
            DeleteResult: Delete result from Pymongo.
        """
        return self.collection.delete_one({"_id": self.id})

    class Meta:
        database: Database
        collection_name: str
        collection_name_generator: Callable
