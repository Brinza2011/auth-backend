from src.repository.user import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_users(self, limit: int = 10, offset: int = 1):
        return await self.repo.find_all(limit=limit, offset=offset)
