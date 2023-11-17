from src.application.spi.db_interface import DbInterface
from src.adapters.spi.db.memory_db import MemoryDB
from src.adapters.spi.db.file_db import FileDB
from .postgres_db import PostgresDB
from src.utils.envs import settings


class Db:
    def __init__(self):
        self.dbs = {
            "postgres": PostgresDB,
            "memory": MemoryDB,
            "file": FileDB,
        }

    def get_db(self) -> DbInterface:
        try:
            return self.dbs[settings.db_type]()

        except KeyError as e:
            raise Exception("Database not found") from e

        except Exception as e:
            raise e

    def get_db_by_type(self) -> DbInterface:
        try:
            return self.dbs[settings.db_type]()

        except KeyError as e:
            raise Exception("Database not found") from e

        except Exception as e:
            raise e
