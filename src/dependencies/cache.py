from src.cache.redis import RedisCache
from src.config import Settings

settings = Settings()


def get_cache() -> RedisCache:
    return RedisCache(
        host="localhost",
        port=6379,
        db=0,
        password=settings.redis_password,
    )
