from src.adapters.spi.repositories.topic_repository import TopicRepository
from src.application.api.controller_interface import ControllerInterface
from src.application.use_cases.topic.edit import TopicEditCase
from src.dto.topic.edit_dto import TopicEditDTO
from fastapi import Request, Response


class TopicEditController(ControllerInterface):
    def __init__(
        self,
        request: Request,
        response: Response,
        repository: TopicRepository,
    ):
        super(TopicEditController, self).__init__(
            request,
            response,
            repository,
        )

        self.repository = repository

    @ControllerInterface.handle_exception
    async def handle(
        self,
        id: str,
        data: TopicEditDTO,
    ) -> dict:
        return {
            "data": TopicEditCase(
                self.repository,
            ).handle(
                data=data,
                id=id,
            ),
        }
