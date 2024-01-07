from src.adapters.spi.repositories.topic_repository import TopicRepository


class TopicDeleteCase:
    def __init__(
        self,
        repository: TopicRepository,
    ):
        self.repository = repository

    def handle(
        self,
        data: str,
    ):
        self.repository.delete(data)
