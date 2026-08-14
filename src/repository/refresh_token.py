from typing import TypedDict

from src.cache.redis import RedisCache


class RefreshTokenModel(TypedDict):
    token: str
    user_id: str
    expires_in: int


class RefreshTokenRepository:
    prefix: str = "refresh_token:"

    def __init__(self, cache: RedisCache):
        self.cache = cache

    def save(self, key: str, value: RefreshTokenModel):
        self.cache.set(
            key=self.prefix + key,
            value=value,
            ex=value.get("expires_in"),
        )

    async def get(self, key: str):
        return self.cache.get(self.prefix + key)

    async def delete(self, key: str):
        self.cache.delete(self.prefix + key)
