from src.application.spi.db_interface import DbInterface


class FileDB(DbInterface):
    db_url = "sqlite:////liquefier/storage/db.db"

    def __init__(self):
        super(FileDB, self).__init__()
