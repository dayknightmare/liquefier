from src.adapters.spi.repository_factory import RepositoryFactory
from src.adapters.spi.stream.consumer import Stream
from fastapi_injector import get_injector_instance
from src.utils.threads import StoppableThread
from src.infra.consumer import StreamReader
from contextlib import asynccontextmanager
from fastapi import FastAPI
import threading


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    injection = get_injector_instance(app)
    repositories = injection.get(RepositoryFactory)
    stream = injection.get(Stream)
    consumer = stream.get_consumer()
    producer = stream.get_producer()
    event = threading.Event()

    reader = StreamReader(
        consumer,
        producer,
        event,
        repositories.get_repositories("topic_repository"),
        repositories.get_repositories("topic_rule_repository"),
    )

    topics = [
        i.name
        for i in repositories.get_repositories("topic_repository").list(
            0,
            None,
        )
    ]

    consumer.subscribe(topics)
    task = StoppableThread(
        event=event,
        target=reader.get_messages,
    )
    task.start()

    app.state.topics = topics

    yield

    stream.close()
    task.stop()
