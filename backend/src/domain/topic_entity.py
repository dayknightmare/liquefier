from dataclasses import dataclass
from pydantic import BaseModel
import datetime


@dataclass(frozen=True)
class TopicEntity(BaseModel):
    id: str
    name: str
    status: int
    created_at: datetime.datetime
