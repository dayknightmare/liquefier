from src.adapters.spi.repositories.topic_rule_repository import TopicRuleRepository
from src.dto.topic_rule.add_dto import TopicRuleAddDTO
from src.domain.topic_entity import TopicEntity


class TopicRuleAddCase:
    def __init__(
        self,
        repository: TopicRuleRepository,
    ):
        self.repository = repository

    def handle(
        self,
        data: TopicRuleAddDTO,
    ) -> TopicEntity | None:
        result = self.repository.add(data)
        self.repository.mapper.to_entity(result)

        return result
