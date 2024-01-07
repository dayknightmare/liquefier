from src.application.mappers.mapper_interface import MapperInterface
from src.application.spi.db_interface import DbInterface
from src.application.spi.db_interface import Base
from typing import Generic, Optional, TypeVar
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import json
import uuid


T = TypeVar("T")


class RepositoryInterface(Generic[T]):
    ormClass: Base  # type: ignore

    def __init__(
        self,
        db: DbInterface,
        ormClass: Base,  # type: ignore
        query_mapper: Optional[MapperInterface] = None,
        no_cache: bool = False,
    ):
        self.db = db
        self.ormClass = ormClass
        self.query_mapper = query_mapper
        self.cache = None if no_cache else self.db.cache
        self.table = self.ormClass.__table__.name

    def add(self, data: BaseModel) -> T:
        with self.db.get_connection() as session:
            value = self.ormClass(
                **{
                    "id": str(uuid.uuid4()),
                    **data.model_dump(),
                }
            )

            session.add(value)
            session.commit()
            session.refresh(value)

            if self.cache is not None:
                self.cache.delete(self.table + ":*")

            return value

    def count(self, no_cache: bool = False) -> int:
        key = "count"
        if self.cache is not None and not no_cache:
            value = self.cache.get(self.table + ":" + key)

            if value is not None:
                return int(value)

        with self.db.get_connection() as session:
            data = (
                session.query(self.ormClass)
                .where(self.ormClass.is_deleted.is_(False))
                .count()
            )

            if self.cache is not None and not no_cache:
                self.cache.set(self.table + ":" + key, str(data))

            return data

    def list(
        self,
        page: int,
        query: BaseModel | None,
        limit: Optional[int] = 25,
        no_cache: bool = False,
    ) -> list[T]:
        limit = limit or 25
        offset = page * limit
        key = ""

        if self.cache is not None and not no_cache:
            key = self.cache.hash_json_key(
                {
                    "limit": limit,
                    "offset": offset,
                    "data": query.model_dump_json(exclude_none=True)
                    if query is not None
                    else "",
                }
            )

            value = self.cache.get(self.table + ":" + key)

            if value is not None:
                result = json.loads(value)
                data = [self.ormClass(**i) for i in result]

                return data

        expressions = []

        if query is not None and self.query_mapper is not None:
            expressions = self.query_mapper.to_orm_query(query)

        with self.db.get_connection() as session:
            data = (
                session.query(self.ormClass)
                .filter(self.ormClass.is_deleted.is_(False))
                .filter(*expressions)
                .order_by(self.ormClass.created_at.desc())
                .offset(offset)
                .limit(limit)
                .all()
            )

        if self.cache is not None and not no_cache:
            result = [jsonable_encoder(i) for i in data]
            self.cache.set(self.table + ":" + key, json.dumps(result))

        return data

    def edit(self, id: str, values: dict):
        if len(values.keys()) < 1:
            return

        with self.db.get_connection() as session:
            session.query(self.ormClass).filter(self.ormClass.id == id).filter(
                self.ormClass.is_deleted.is_(False)
            ).update(values)
            session.commit()

            if self.cache is not None:
                self.cache.delete(self.table + ":*")

    def get(self, id: str) -> T | None:
        with self.db.get_connection() as session:
            data = (
                session.query(self.ormClass)
                .filter(self.ormClass.id == id)
                .filter(self.ormClass.is_deleted.is_(False))
                .first()
            )

        return data

    def delete(self, id: str):
        with self.db.get_connection() as session:
            session.query(self.ormClass).filter(self.ormClass.id == id).filter(
                self.ormClass.is_deleted.is_(False)
            ).update(
                {
                    self.ormClass.is_deleted: True,
                }
            )
            session.commit()

            if self.cache is not None:
                self.cache.delete(self.table + ":*")
