from src.adapters.spi.repositories.topic_repository import TopicRepository
from src.domain.topic_entity import TopicEntity


class TopicDetailCase:
    def __init__(
        self,
        repository: TopicRepository,
    ):
        self.repository = repository

    def handle(
        self,
        id: str,
    ) -> TopicEntity | None:
        result = self.repository.get(id)

        if result is None:
            return None

        self.repository.mapper.to_entity(result)

        return result
