from src.application.spi.cache_interface import CacheInterface
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator, Optional
from sqlalchemy import create_engine
from abc import ABC
import contextlib


Base = declarative_base()


class DbInterface(ABC):
    db_url = ""
    cache: Optional[CacheInterface] = None

    def __init__(self, cache: Optional[CacheInterface] = None):
        self.engine = create_engine(
            self.db_url,
            pool_size=20,
            pool_recycle=60 * 5,
            pool_pre_ping=True,
        )

        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )

        self.cache = cache

    @contextlib.contextmanager
    def get_connection(self) -> Generator[Session, None, None]:
        db = self.SessionLocal()

        try:
            yield db

        finally:
            db.close()
