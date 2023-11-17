from src.application.repositories.repository_interface import RepositoryInterface
from src.adapters.spi.mappers.topic_mapper import TopicMapper, TopicQueryMapper
from src.application.spi.db_interface import DbInterface
from src.models.topic import Topic


class TopicRepository(RepositoryInterface[Topic]):
    def __init__(self, db: DbInterface):
        self.mapper = TopicMapper()
        self.query_mapper = TopicQueryMapper()

        super(TopicRepository, self).__init__(
            db,
            Topic,
            self.query_mapper,
        )
