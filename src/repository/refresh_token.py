


from typing import TypedDict

import redis

from src.cache.redis import RedisCache

class RefreshTokenModel(TypedDict):
    token: str
    user_id: str
    expires_in: int

class RefreshTokenRepository:
    prefix: str = "refresh_token:"

    def __init__(self, cache: RedisCache):
        self.cache = cache

    async def set(self, key: str, value: RefreshTokenModel):
        self.cache.hset(self.prefix + key, value)

    async def get(self, key: str):
        return self.cache.hget(self.prefix + key)
