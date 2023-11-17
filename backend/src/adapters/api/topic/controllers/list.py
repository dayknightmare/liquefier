from src.adapters.spi.repositories.topic_repository import TopicRepository
from src.application.api.controller_interface import ControllerInterface
from src.application.use_cases.topic.list import TopicListCase
from src.dto.topic.list_dto import TopicListDTO
from fastapi import Request, Response


class TopicListController(ControllerInterface):
    def __init__(
        self,
        request: Request,
        response: Response,
        repository: TopicRepository,
    ):
        super(TopicListController, self).__init__(
            request,
            response,
            repository,
        )

        self.repository = repository

    @ControllerInterface.handle_exception
    async def handle(
        self,
        query: TopicListDTO,
        page: int | None = 0,
    ) -> dict:
        return {
            "data": TopicListCase(
                self.repository,
            ).handle(
                query,
                max(page or 0, 0),
            )
        }
