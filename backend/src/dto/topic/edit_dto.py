from pydantic import BaseModel
from typing import Literal


class TopicEditDTO(BaseModel):
    status: Literal[1, 0]
