from src.application.spi.cache_interface import CacheInterface
from redis.cluster import RedisCluster
from src.utils.envs import settings
from redis import Redis


class RedisCache(CacheInterface):
    connection: Redis | RedisCluster
    prefix = "liquefier:"

    def __init__(self):
        super(RedisCache, self).__init__()
        self.start_connection()

    def start_connection(self):
        if settings.is_redis_cluster:
            self.connection: RedisCluster | Redis = RedisCluster(
                host=settings.redis_host or "localhost",
                port=settings.redis_port or 6379,
                decode_responses=True,
            )

            return

        self.connection: RedisCluster | Redis = Redis(
            host=settings.redis_host or "localhost",
            port=settings.redis_port or 6379,
            decode_responses=True,
        )

    def get(self, key: str) -> str | None:
        return self.connection.get(self.prefix + key)  # type: ignore

    def set(self, key: str, value: str) -> bool | None:
        return self.connection.setex(
            self.prefix + key,
            60 * 15,
            value,
        )  # type: ignore

    def delete(self, key: str) -> bool:
        if "*" in key:
            keys = self.connection.scan_iter(self.prefix + key)

            for i in keys:
                self.connection.delete(i)  # type: ignore

            return True

        self.connection.delete(self.prefix + key)  # type: ignore

        return True
