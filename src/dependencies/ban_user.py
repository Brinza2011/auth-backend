from fastapi import Depends
from src.dependencies.token import get_refresh_token_repo
from src.repository.refresh_token import RefreshTokenRepository
from src.service.ban import BanUserService


async def get_ban_user_service(
    refresh_token_repo: RefreshTokenRepository = Depends(get_refresh_token_repo),
) -> BanUserService:
    return BanUserService(refresh_token_repo)
