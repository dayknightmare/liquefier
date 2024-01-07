from src.adapters.spi.repositories.topic_repository import TopicRepository
from src.application.api.controller_interface import ControllerInterface
from src.application.use_cases.topic.delete import TopicDeleteCase
from fastapi import Request, Response


class TopicDeleteController(ControllerInterface):
    def __init__(
        self,
        request: Request,
        response: Response,
        repository: TopicRepository,
    ):
        super(TopicDeleteController, self).__init__(
            request,
            response,
            repository,
        )

        self.repository = repository

    @ControllerInterface.handle_exception
    async def handle(self, id: str) -> dict:
        TopicDeleteCase(self.repository).handle(data=id)

        return {
            "data": "ok",
        }
