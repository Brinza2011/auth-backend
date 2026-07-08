from sqlalchemy import select

from src.database.db import SessionType
from src.exceptions.user_not_found import UserNotFoundException
from src.models.user import UserModel


class UserRepository:
    def __init__(self, session: SessionType) -> None:
        self.session: SessionType = session

    async def find_all(self, limit: int = 10, offset: int = 1):
        stmt = (
            select(UserModel)
            .order_by(UserModel.id)
            # .offset((offset - 1) * limit)
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_user(self, username: str, password: str, email: str) -> UserModel:

        user = UserModel(username=username, password=password, email=email)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get_by_username(self, username: str) -> UserModel | None:

        stmt = select(UserModel).where(UserModel.username == username)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> UserModel | None:

        stmt = select(UserModel).where(UserModel.email == email)

        result = await self.session.execute(stmt)

        user = result.scalar_one_or_none()

        return user

    async def get_user_by_id(self, user_id: int) -> UserModel | None:

        stmt = select(UserModel).where(UserModel.id == user_id)

        result = await self.session.execute(stmt)

        user = result.scalar_one_or_none()

        return user

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user_by_id(user_id)

        if not user:
            raise UserNotFoundException()

        await self.session.delete(user)
        await self.session.commit()
