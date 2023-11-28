from src.adapters.spi.repositories.topic_rule_repository import TopicRuleRepository
from src.application.api.controller_interface import ControllerInterface
from src.application.use_cases.topic_rule.add import TopicRuleAddCase
from src.dto.topic_rule.add_dto import TopicRuleAddDTO
from fastapi import Request, Response


class TopicRuleAddController(ControllerInterface):
    def __init__(
        self,
        request: Request,
        response: Response,
        repository: TopicRuleRepository,
    ):
        super(TopicRuleAddController, self).__init__(
            request,
            response,
            repository,
        )

        self.repository = repository

    @ControllerInterface.handle_exception
    async def handle(
        self,
        data: TopicRuleAddDTO,
    ) -> dict:
        result = TopicRuleAddCase(
            self.repository,
        ).handle(data)

        if result is None:
            self.response.status_code = 400

            return {"error": "Topic rule already exists"}

        return {"data": result}
