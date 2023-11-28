from src.adapters.spi.repositories.topic_rule_repository import TopicRuleRepository
from src.application.use_cases.topic_rule.list import TopicRuleListCase
from src.application.api.controller_interface import ControllerInterface
from src.dto.topic_rule.list_dto import TopicRuleListDTO
from fastapi import Request, Response


class TopicRuleListController(ControllerInterface):
    def __init__(
        self,
        request: Request,
        response: Response,
        repository: TopicRuleRepository,
    ):
        super(TopicRuleListController, self).__init__(
            request,
            response,
            repository,
        )

        self.repository = repository

    @ControllerInterface.handle_exception
    async def handle(
        self,
        query: TopicRuleListDTO,
        page: int | None = 0,
    ) -> dict:
        return {
            "data": TopicRuleListCase(
                self.repository,
            ).handle(
                query,
                max(page or 0, 0),
            )
        }
