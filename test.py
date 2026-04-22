from src.database.db import get_session
from src.repository.user import UserRepository
import asyncio


async def get_user_repo():
    async for session in get_session():
        repo = UserRepository(session=session)

        print([user.email for user in await repo.find_all()])


if __name__ == "__main__":
    asyncio.run(get_user_repo())