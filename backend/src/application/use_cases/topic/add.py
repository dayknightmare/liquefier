from src.adapters.spi.repositories.topic_repository import TopicRepository
from src.domain.topic_entity import TopicEntity
from src.dto.topic.add_dto import TopicAddDTO


class TopicAddCase:
    def __init__(
        self,
        repository: TopicRepository,
    ):
        self.repository = repository

    def handle(
        self,
        data: TopicAddDTO,
    ) -> TopicEntity:
        result = self.repository.add(data)
        self.repository.mapper.to_entity(result)

        return result
