from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, Optional
from functools import lru_cache


class Settings(BaseSettings):
    debug: bool = True

    internal_token: str = (
        "dcb0482933fe54d38207c5fea9ec1a4754636edf7a07667e29570de8113400ff"
    )

    db_type: Literal["postgres", "file", "memory"] = "postgres"
    db_user: Optional[str] = None
    db_pass: Optional[str] = None
    db_port: Optional[int] = 5432
    db_host: Optional[str] = None

    kafka_hosts: str = "localhost:9092"

    use_cache: bool = True
    redis_host: Optional[str] = None
    redis_port: Optional[int] = None

    jwt_secret: str

    version: str = "1.0.0"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore


settings = get_settings()
