from src.adapters.spi.repositories.topic_repository import TopicRepository
from src.application.api.controller_interface import ControllerInterface
from src.application.use_cases.topic.add import TopicAddCase
from src.adapters.spi.stream.consumer import Stream
from src.dto.topic.add_dto import TopicAddDTO
from fastapi import Request, Response


class TopicAddController(ControllerInterface):
    def __init__(
        self,
        request: Request,
        response: Response,
        repository: TopicRepository,
    ):
        super(TopicAddController, self).__init__(
            request,
            response,
            repository,
        )

        self.repository = repository

    @ControllerInterface.handle_exception
    async def handle(
        self,
        data: TopicAddDTO,
        stream: Stream,
    ) -> dict:
        result = TopicAddCase(
            self.repository,
        ).handle(data)

        topics: list[str] = self.request.app.state.topics
        topics.append(result.name)

        consumer = stream.get_consumer()
        consumer.subscribe(topics)

        self.request.app.state.topics = topics

        return {"data": result}
