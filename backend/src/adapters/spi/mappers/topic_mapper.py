from src.application.mappers.mapper_interface import MapperInterface
from src.domain.topic_entity import TopicEntity
from src.dto.topic.list_dto import TopicListDTO
from sqlalchemy import BinaryExpression
from src.models.topic import Topic


class TopicMapper(MapperInterface):
    def __init__(self):
        super(TopicMapper, self).__init__()

    def to_entity(self, model: Topic) -> TopicEntity:
        return TopicEntity(
            id=model.id,  # type: ignore
            name=model.name,  # type: ignore
            status=model.status,  # type: ignore
            created_at=model.created_at,  # type: ignore
        )


class TopicQueryMapper(MapperInterface):
    def __init__(self):
        super(TopicQueryMapper, self).__init__()

    def to_orm_query(self, data: TopicListDTO) -> list[BinaryExpression]:
        values = data.model_dump(exclude_none=True)

        fields = {
            "filter_id": Topic.id,
            "filter_name": Topic.name,
            "filter_status": Topic.status,
        }

        result: list[BinaryExpression] = []

        for i in values:
            field = fields[i]

            result.append(
                self.alloweds_filters[values[i]["op"]](field, values[i]["value"]),
            )

        return result
