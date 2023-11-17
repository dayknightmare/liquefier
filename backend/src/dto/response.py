from typing import TypeVar, Generic
from pydantic import BaseModel


T = TypeVar("T")


class ErrorResponseDTO(BaseModel):
    error: str


class SucessResponseDTO(BaseModel, Generic[T]):
    data: T
