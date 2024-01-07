from src.application.spi.cache_interface import CacheInterface
from src.application.spi.db_interface import DbInterface
from typing import Optional


class FileDB(DbInterface):
    db_url = "sqlite:////liquefier/storage/db.db"

    def __init__(self, cache: Optional[CacheInterface] = None):
        super(FileDB, self).__init__(cache)
