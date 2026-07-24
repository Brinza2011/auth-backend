


from src.cache.redis import RedisCache


def get_cache() -> RedisCache:
    return RedisCache(
        host="localhost",
        port=6379,
        db=0,
        password="12345678abcd",
    )
