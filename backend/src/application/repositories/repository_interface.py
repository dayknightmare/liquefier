from src.application.mappers.mapper_interface import MapperInterface
from src.application.spi.db_interface import DbInterface
from typing import Callable, Generic, Optional, TypeVar
from pydantic import BaseModel
import uuid


T = TypeVar("T")


class RepositoryInterface(Generic[T]):
    def __init__(
        self,
        db: DbInterface,
        ormClass: Callable,
        query_mapper: MapperInterface,
    ):
        self.db = db
        self.ormClass = ormClass
        self.query_mapper = query_mapper

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

            return value

    def list(
        self,
        page: int,
        query: BaseModel | None,
        limit: Optional[int] = 25,
    ) -> list[T]:
        limit = limit or 25
        offset = page * limit
        expressions = []

        if query is not None:
            expressions = self.query_mapper.to_orm_query(query)

        with self.db.get_connection() as session:
            data = (
                session.query(self.ormClass)
                .filter(self.ormClass.is_deleted.is_(False))
                .filter(*expressions)
                .offset(offset)
                .limit(limit)
                .all()
            )

        return data

    def edit(self, id: str, values: dict):
        if len(values.keys()) < 1:
            return

        with self.db.get_connection() as session:
            session.query(self.ormClass).filter(self.ormClass.id == id).filter(
                self.ormClass.is_deleted.is_(False)
            ).update(values)
            session.commit()

    def get(self, id: str) -> T | None:
        with self.db.get_connection() as session:
            data = (
                session.query(self.ormClass)
                .filter(self.ormClass.id == id)
                .filter(self.ormClass.is_deleted.is_(False))
                .first()
            )

        if data:
            return data

        return None

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
