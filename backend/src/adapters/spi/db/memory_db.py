from src.application.spi.db_interface import DbInterface


class MemoryDB(DbInterface):
    db_url = "sqlite://"

    def __init__(self):
        super(MemoryDB, self).__init__()
