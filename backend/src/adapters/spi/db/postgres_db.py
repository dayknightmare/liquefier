from src.application.spi.db_interface import DbInterface
from src.utils.envs import settings


class PostgresDB(DbInterface):
    db_url = (
        "postgresql+psycopg2://"
        + f"{settings.db_user}:{settings.db_pass}@{settings.db_host}/liquefier"
    )

    def __init__(self):
        super(PostgresDB, self).__init__()
