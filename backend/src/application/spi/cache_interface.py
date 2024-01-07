from typing import Any
from abc import ABC
import hashlib
import json


class CacheInterface(ABC):
    connection: Any

    def hash_json_key(self, key: dict[str, Any]) -> str:
        return hashlib.sha256(json.dumps(key, default=str).encode("utf-8")).hexdigest()

    def get(self, key: str) -> str | None:
        raise NotImplementedError()

    def set(self, key: str, value: str) -> bool:
        raise NotImplementedError()

    def delete(self, key: str) -> bool:
        raise NotImplementedError()
