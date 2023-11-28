from src.adapters.spi.mappers.topic_rule_mapper import (
    TopicRuleMapper,
    TopicRuleQueryMapper,
)
from src.application.repositories.repository_interface import RepositoryInterface
from src.application.spi.db_interface import DbInterface
from src.models.topic_rule import TopicRule


class TopicRuleRepository(RepositoryInterface[TopicRule]):
    def __init__(self, db: DbInterface):
        self.mapper = TopicRuleMapper()
        self.query_mapper = TopicRuleQueryMapper()

        super(TopicRuleRepository, self).__init__(
            db,
            TopicRule,
            self.query_mapper,
        )

    def get_by_topic_id(self, id: str) -> TopicRule | None:
        with self.db.get_connection() as session:
            data = (
                session.query(TopicRule)
                .filter(TopicRule.topic_id == id)
                .filter(TopicRule.is_deleted.is_(False))
                .first()
            )

        if data:
            return data

        return None
