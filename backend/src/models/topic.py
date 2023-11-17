from sqlalchemy import Column, DateTime, Integer, String, Boolean
from src.application.spi.db_interface import Base
import datetime


class Topic(Base):
    __tablename__ = "topic"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(180))
    status = Column(Integer(), index=True, default=1)
    created_at = Column(DateTime(), index=True, default=datetime.datetime.utcnow)
    is_deleted = Column(Boolean(), index=True, default=False)
