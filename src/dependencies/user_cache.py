from src.cache.redis import RedisCache
from src.database.db import get_session
from src.dependencies.cache import get_cache
from src.service.user_caches import UserCacheService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.repository.user import UserRepository


async def get_user_cache(
    session: AsyncSession = Depends(get_session), cache: RedisCache = Depends(get_cache)
) -> UserCacheService:
    repo = UserRepository(session)

    return UserCacheService(
        repo=repo,
        cache=cache,
    )
