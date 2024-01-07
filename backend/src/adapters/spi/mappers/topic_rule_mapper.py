from src.application.mappers.mapper_interface import MapperInterface
from src.dto.topic_rule.list_dto import TopicRuleListDTO
from src.domain.topic_rule_entity import TopicRuleEntity
from src.models.topic_rule import TopicRule
from sqlalchemy import BinaryExpression


class TopicRuleMapper(MapperInterface):
    def __init__(self):
        super(TopicRuleMapper, self).__init__()

    def to_entity(self, model: TopicRule) -> TopicRuleEntity:
        return TopicRuleEntity(
            id=model.id,  # type: ignore
            topic_id=model.topic_id,  # type: ignore
            transformers=model.transformers,  # type: ignore
            output=model.output,  # type: ignore
            extras=model.extras,  # type: ignore
            status=model.status,  # type: ignore
            name=model.name,  # type: ignore
            created_at=model.created_at,  # type: ignore
        )


class TopicRuleQueryMapper(MapperInterface):
    def __init__(self):
        super(TopicRuleQueryMapper, self).__init__()

    def to_orm_query(self, data: TopicRuleListDTO) -> list[BinaryExpression]:
        values = data.model_dump(exclude_none=True)

        fields = {
            "filter_id": TopicRule.id,
            "filter_topic_id": TopicRule.topic_id,
            "filter_status": TopicRule.status,
            "filter_output": TopicRule.output,
            "filter_name": TopicRule.name,
        }

        result: list[BinaryExpression] = []

        for i in values:
            field = fields[i]

            result.append(
                self.alloweds_filters[values[i]["op"]](field, values[i]["value"]),
            )

        return result
