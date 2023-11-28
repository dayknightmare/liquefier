from typing import Literal
from pydantic import BaseModel


class TopicRuleAddDTO(BaseModel):
    topic_id: str
    transformers: list[str]
    output: Literal["kafka", "file"]
    extras: dict
