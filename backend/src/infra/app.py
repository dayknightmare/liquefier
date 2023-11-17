from src.adapters.spi.repository_factory import RepositoryFactory
from src.adapters.api.topic.router import topic_router
from src.adapters.spi.stream.consumer import Stream
from injector import Injector, SingletonScope
from fastapi_injector import attach_injector
from src.infra.lifespan import lifespan
from src.adapters.spi.db.db import Db
from fastapi import FastAPI


def create_app(injector: Injector) -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    db = Db()
    stream = Stream()

    fact = RepositoryFactory(db=db.get_db())

    injector.binder.bind(RepositoryFactory, to=fact, scope=SingletonScope)
    injector.binder.bind(Stream, to=stream, scope=SingletonScope)

    app.include_router(topic_router, tags=["Topic"])

    attach_injector(app, injector)

    return app
