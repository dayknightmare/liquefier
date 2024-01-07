from src.application.spi.cache_interface import CacheInterface
from src.application.spi.db_interface import DbInterface
from typing import Optional


class MemoryDB(DbInterface):
    db_url = "sqlite://"

    def __init__(self, cache: Optional[CacheInterface] = None):
        super(MemoryDB, self).__init__(cache)
