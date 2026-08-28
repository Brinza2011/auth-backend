from src.repository.refresh_token import RefreshTokenRepository


class BanUserService:
    def __init__(self, refresh_token_repo: RefreshTokenRepository):
        self._refresh_token_repo = refresh_token_repo

    async def ban_user(self, user_id: str) -> None:
        await self._refresh_token_repo.delete(user_id)

    async def is_banned(self, user_id: str) -> bool:
        return await self._refresh_token_repo.get(user_id) is not None
