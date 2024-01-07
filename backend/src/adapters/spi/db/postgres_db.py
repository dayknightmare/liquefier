from src.application.spi.cache_interface import CacheInterface
from src.application.spi.db_interface import DbInterface
from src.utils.envs import settings
from typing import Optional


class PostgresDB(DbInterface):
    db_url = (
        "postgresql+psycopg2://"
        + f"{settings.db_user}:{settings.db_pass}@{settings.db_host}/liquefier"
    )

    def __init__(self, cache: Optional[CacheInterface] = None):
        super(PostgresDB, self).__init__(cache)
