

import json
import redis


class RedisCache:
    def __init__(self, host: str, port: int, db: int, password: str):
        self._redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True,
        )

    def get(self, key: str):
        value = self._redis.get(key)
        return json.loads(value) if value else None

    def set(self, key: str, value, ex: int | None = 300):
        self._redis.set(
            key,
            json.dumps(value),
            ex=ex,
        )
