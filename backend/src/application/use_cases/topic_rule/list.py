from src.adapters.spi.repositories.topic_rule_repository import TopicRuleRepository
from src.domain.topic_rule_entity import TopicRuleEntity
from src.dto.topic_rule.list_dto import TopicRuleListDTO


class TopicRuleListCase:
    def __init__(
        self,
        repository: TopicRuleRepository,
    ):
        self.repository = repository

    def handle(
        self,
        query: TopicRuleListDTO,
        page: int,
    ) -> list[TopicRuleEntity]:
        return [
            self.repository.mapper.to_entity(i)
            for i in self.repository.list(page, query)
        ]
