from src.adapters.spi.repositories.topic_repository import TopicRepository
from src.dto.topic.edit_dto import TopicEditDTO
from src.domain.topic_entity import TopicEntity
from src.models.topic import Topic


class TopicEditCase:
    def __init__(
        self,
        repository: TopicRepository,
    ):
        self.repository = repository

    def handle(
        self,
        data: TopicEditDTO,
        id: str,
    ) -> TopicEntity | None:
        fields = {
            "status": Topic.status,
        }

        values = data.model_dump(exclude_unset=True)

        self.repository.edit(
            id,
            {fields[i]: values[i] for i in values},
        )

        result = self.repository.get(id)

        if result is None:
            return None

        return self.repository.mapper.to_entity(result)
