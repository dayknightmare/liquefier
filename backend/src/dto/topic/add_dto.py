from pydantic import BaseModel


class TopicAddDTO(BaseModel):
    name: str
