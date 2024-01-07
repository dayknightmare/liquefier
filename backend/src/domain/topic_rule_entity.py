from dataclasses import dataclass
from pydantic import BaseModel
from typing import Literal
import datetime


@dataclass(frozen=True)
class TopicRuleEntity(BaseModel):
    id: str
    topic_id: str
    transformers: list[str]
    output: Literal["kafka", "file", "none"]
    extras: dict
    status: int
    name: str
    created_at: datetime.datetime
