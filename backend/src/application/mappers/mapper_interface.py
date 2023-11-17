from sqlalchemy import BinaryExpression
from pydantic import BaseModel


class MapperInterface:
    alloweds_filters = {
        "eql": lambda x, y: x == y,
        "neql": lambda x, y: x != y,
        "lt": lambda x, y: x < y,
        "lte": lambda x, y: x <= y,
        "gt": lambda x, y: x > y,
        "gte": lambda x, y: x >= y,
        "null": lambda x, _: x.is_(None),
        "notnull": lambda x, _: x.is_not(None),
        "like": lambda x, y: x.like(y),
    }

    def to_orm_query(self, _: BaseModel) -> list[BinaryExpression]:
        raise NotImplementedError
