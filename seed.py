import asyncio

from src.database.db import Base, get_session, engine
from src.models.user import UserModel

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



async def users_mock():
    async for session in get_session():
        # Пример запроса
        # result = await session.execute(select(User))
        banan = UserModel(
            username = "User1",
            password = "1234",
            email = "Not_user15668@gmail.com",
            role = "ADMIN"
        )

        tasya = UserModel(
            username = "User2",
            password = "134488",
            email = "Tasyasuper34@gmail.com",
            role = "USER"
        )

        andrey = UserModel(
            username = "User3",
            password = "156790",
            email = "AndreyGolovkin42@gmail.com",
            role = "USER"
        )

        session.add_all([banan, tasya, andrey])
        await session.commit()

        print("Сессия открыта и готова к работе")


async def main():
    await init_db()
    await users_mock()


if __name__ == "__main__":
    asyncio.run(main())
