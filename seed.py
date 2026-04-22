import asyncio
from src.database.db import get_session
from src.models.user import User

async def users_mock():
    async for session in get_session():
        # Пример запроса
        # result = await session.execute(select(User))
        banan = User(
            username = "User1",
            password = "1234",
            email = "Not_user15668@gmail.com"
        )

        tasya = User(
            username = "User2",
            password = "134488",
            email = "Tasyasuper34@gmail.com"
        )

        andrey = User(
            username = "User1",
            password = "156790",
            email = "AndreyGolovkin42@gmail.com"
        )

        session.add_all([banan, tasya, andrey])
        await session.commit()

        print("Сессия открыта и готова к работе")


async def main():
    await users_mock()


if __name__ == "__main__":
    asyncio.run(main())
