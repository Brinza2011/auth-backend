



from typing import TypedDict
from src.cache import redis

class RefreshTokenModel(TypedDict):
    def __init__(self, token: str, user_id: str, expires_in: str):
        self.token =token
        self.user_id = user_id
        self.expires_in = expires_in


class RefreshTokenRepo:
    prefix: str = "refresh_token:"

    def __init__(self, cache: redis.Redis):
        self.cache = cache

    async def set(self, key: str, value: str, ttl: int = 300):
        self.cache.hset(self.prefix + key, value, ttl)

    async def get(self, key: str):
        return self.cache.hget(self.prefix + key)
