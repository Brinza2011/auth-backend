from src.cache.redis import RedisCache
from src.database.db import get_session
from src.service.user_caches import UserCacheService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.repository.user import UserRepository


async def get_user_cache(
    session: AsyncSession = Depends(get_session),
) -> UserCacheService:
    repo = UserRepository(session)

    cache = RedisCache(
        host="127.0.0.1",
        port=6379,
        db=0,
        password="12345678abcd",
    )

    return UserCacheService(
        repo=repo,
        cache=cache,
    )
