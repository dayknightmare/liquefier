from src.application.spi.cache_interface import CacheInterface
from src.application.spi.db_interface import DbInterface
from src.adapters.spi.db.postgres_db import PostgresDB
from src.adapters.spi.db.memory_db import MemoryDB
from src.adapters.spi.db.file_db import FileDB
from src.utils.envs import settings
from typing import Optional


class Db:
    def __init__(self, cache: Optional[CacheInterface] = None):
        self.dbs = {
            "postgres": PostgresDB,
            "memory": MemoryDB,
            "file": FileDB,
        }

        self.cache = cache

    def get_db(self) -> DbInterface:
        try:
            return self.dbs[settings.db_type](self.cache)

        except KeyError as e:
            raise Exception("Database not found") from e

        except Exception as e:
            raise e
