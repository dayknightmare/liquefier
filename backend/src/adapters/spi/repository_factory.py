from .repositories.topic_repository import TopicRepository
from src.application.spi.db_interface import DbInterface


class RepositoryFactory:
    def __init__(self, db: DbInterface):
        self.__db = db
        self.__repositories = {
            "topic_repository": TopicRepository(self.__db),
        }

    def get_repositories(self, name: str):
        if name in self.__repositories:
            return self.__repositories[name]

        else:
            raise Exception("Repository does not exist")
