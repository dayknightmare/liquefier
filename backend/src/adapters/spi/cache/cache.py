from src.application.spi.cache_interface import CacheInterface
from src.adapters.spi.cache.redis_cache import RedisCache
from src.utils.envs import settings


class Cache:
    def __init__(self):
        self.caches = {
            "redis": RedisCache,
        }

    def get_cache(self) -> CacheInterface | None:
        if not settings.use_cache:
            return

        try:
            return self.caches["redis"]()

        except KeyError as e:
            raise Exception("Cache not found") from e

        except Exception as e:
            raise e
