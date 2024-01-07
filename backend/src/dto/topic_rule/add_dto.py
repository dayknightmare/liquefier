from pydantic import BaseModel
from typing import Literal


class TopicRuleAddDTO(BaseModel):
    topic_id: str
    transformers: list[str]
    output: Literal["kafka", "file", "none"]
    extras: dict
    name: str
