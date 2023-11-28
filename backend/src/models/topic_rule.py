from sqlalchemy import JSON, Column, DateTime, Integer, String, Boolean
from src.application.spi.db_interface import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKey
import datetime


class TopicRule(Base):
    __tablename__ = "topic_rule"

    id = Column(String(36), primary_key=True, index=True)
    topic_id: Mapped[str] = mapped_column(
        ForeignKey("topic.id"), index=True, unique=True
    )
    transformers = Column(JSON(), nullable=True)
    output = Column(String(100))
    extras = Column(JSON(), nullable=True)
    status = Column(Integer(), index=True, default=1)
    created_at = Column(DateTime(), index=True, default=datetime.datetime.utcnow)
    is_deleted = Column(Boolean(), index=True, default=False)
