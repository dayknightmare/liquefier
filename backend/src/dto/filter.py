from typing import TypeVar, Generic, Literal
from pydantic import BaseModel


T = TypeVar("T")
Y = TypeVar(
    "Y",
    bound=Literal[
        "lt",
        "lte",
        "gt",
        "gte",
        "eql",
        "like",
        "null",
        "notnull",
        "neql",
    ],
)


class Filter(BaseModel, Generic[T, Y]):
    op: Y
    value: T
