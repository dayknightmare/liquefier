from typing import Optional, Literal
from src.dto.filter import Filter
from pydantic import BaseModel


class TopicRuleListDTO(BaseModel):
    filter_id: Optional[Filter[str, Literal["eql"]]] = None
    filter_topic_id: Optional[Filter[str, Literal["eql"]]] = None
    filter_status: Optional[Filter[int, Literal["eql"]]] = None
    filter_output: Optional[Filter[Literal["kafka", "file"], Literal["eql"]]] = None
