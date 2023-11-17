from src.adapters.spi.repositories.topic_repository import TopicRepository
from src.application.api.controller_interface import ControllerInterface
from src.application.use_cases.topic.detail import TopicDetailCase
from src.domain.topic_entity import TopicEntity
from fastapi import Request, Response


class TopicDetailController(ControllerInterface):
    def __init__(
        self,
        request: Request,
        response: Response,
        repository: TopicRepository,
    ):
        super(TopicDetailController, self).__init__(
            request,
            response,
            repository,
        )

        self.repository = repository

    @ControllerInterface.handle_exception
    async def handle(
        self,
        id: str,
    ) -> dict[str, TopicEntity | None]:
        return {
            "data": TopicDetailCase(
                self.repository,
            ).handle(id),
        }
