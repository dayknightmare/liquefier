from typing import Optional, Literal
from src.dto.filter import Filter
from pydantic import BaseModel


class TopicListDTO(BaseModel):
    filter_id: Optional[Filter[str, Literal["eql"]]] = None
    filter_name: Optional[Filter[str, Literal["like", "eql"]]] = None
    filter_status: Optional[Filter[int, Literal["eql"]]] = None
