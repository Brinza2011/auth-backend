from fastapi import Depends

from src.cache.redis import RedisCache
from src.dependencies.cache import get_cache
from src.service.jwt import JWTService
from src.service.token import TokenService
from src.dependencies.jwt import get_jwt_service
from src.repository.refresh_token import RefreshTokenRepository


async def get_refresh_token_repo(
    cache: RedisCache = Depends(get_cache),
) -> RefreshTokenRepository:
    return RefreshTokenRepository(cache)


async def get_token_service(
    refresh_token_repo: RefreshTokenRepository = Depends(get_refresh_token_repo),
    jwt_svc: JWTService = Depends(get_jwt_service),
) -> TokenService:
    token_svc = TokenService(jwt_svc, refresh_token_repo)
    return token_svc
