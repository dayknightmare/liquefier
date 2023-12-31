from src.adapters.spi.repository_factory import RepositoryFactory
from src.adapters.api.topic_rule.router import topic_rule_router
from src.adapters.api.topic.router import topic_router
from src.adapters.spi.stream.consumer import Stream
from src.adapters.spi.cache.cache import Cache
from injector import Injector, SingletonScope
from fastapi_injector import attach_injector
from src.infra.lifespan import lifespan
from src.adapters.spi.db.db import Db
from fastapi import FastAPI


def create_app(injector: Injector) -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    cache = Cache()
    db = Db(cache.get_cache())
    stream = Stream()

    fact = RepositoryFactory(db=db.get_db())

    injector.binder.bind(RepositoryFactory, to=fact, scope=SingletonScope)
    injector.binder.bind(Stream, to=stream, scope=SingletonScope)

    app.include_router(topic_router, tags=["Topic"])
    app.include_router(topic_rule_router, tags=["Topic Rule"])

    attach_injector(app, injector)

    return app
