# import asyncio

# from src.database.db import Base, get_session, engine
# from src.models.user import UserModel


# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# async def users_mock():
#     async for session in get_session():
#         # Пример запроса
#         # result = await session.execute(select(User))
#         #

#         banan = UserModel(
#             username="User1",
#             password="1234",
#             email="Not_user15668@gmail.com",
#             role="ADMIN",
#         )

#         tasya = UserModel(
#             username="User2",
#             password="134488",
#             email="Tasyasuper34@gmail.com",
#             role="ADMIN",
#         )

#         andrey = UserModel(
#             username="User3",
#             password="156790",
#             email="AndreyGolovkin42@gmail.com",
#             role="USER",
#         )

#         session.add_all([banan, tasya, andrey])
#         await session.commit()

#         print("Сессия открыта и готова к работе")


# async def main():
#     await init_db()
#     await users_mock()


# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
import random
import string

from src.database.db import Base, get_session, engine
from src.models.user import UserModel

ROLES = ["ADMIN", "USER"]


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def random_password(length: int = 10) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


async def users_mock(count: int = 5000):
    async for session in get_session():
        users = []

        for i in range(1, count + 1):
            username = f"user_{i}"
            email = f"user_{i}_{random.randint(100000, 999999)}@example.com"

            user = UserModel(
                username=username,
                password=random_password(),
                email=email,
                role=random.choice(ROLES),
            )

            users.append(user)

        session.add_all(users)
        await session.commit()

        print(f"Добавлено {count} пользователей")


async def main():
    await init_db()
    await users_mock()


if __name__ == "__main__":
    asyncio.run(main())
