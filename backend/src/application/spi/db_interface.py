from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from typing import Generator
from abc import ABC
import contextlib


Base = declarative_base()


class DbInterface(ABC):
    db_url = ""

    def __init__(self):
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

    @contextlib.contextmanager
    def get_connection(self) -> Generator[Session, None, None]:
        db = self.SessionLocal()

        try:
            yield db

        finally:
            db.close()
