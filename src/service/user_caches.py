from src.cache.redis import RedisCache
from src.repository.user import UserRepository


class UserCacheService:
    def __init__(self, repo: UserRepository, cache: RedisCache) -> None:
        self.repo = repo
        self.cache = cache

    async def get_admin_users(self):
        cache_users = self.cache.get("admin_users")

        if cache_users:
            return cache_users

        users = await self.repo.find_all()

        admins = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            }
            for user in users
            if user.role == "ADMIN"
        ]

        self.cache.set(
            "admin_users",
            admins,
            ex=60,
        )

        return admins
