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
        topic_rule = self.repository.get_by_topic_id(data.topic_id)

        if topic_rule is not None:
            return None

        result = self.repository.add(data)
        self.repository.mapper.to_entity(result)

        return result
