from src.adapters.spi.repositories.topic_repository import TopicRepository
from src.domain.topic_entity import TopicEntity
from src.dto.topic.list_dto import TopicListDTO


class TopicListCase:
    def __init__(
        self,
        repository: TopicRepository,
    ):
        self.repository = repository

    def handle(
        self,
        query: TopicListDTO,
        page: int,
    ) -> list[TopicEntity]:
        return [
            self.repository.mapper.to_entity(i)
            for i in self.repository.list(page, query)
        ]
