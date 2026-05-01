from sqlalchemy import select
from src.database.db import SessionType
from src.models.user import User

class UserRepository:
    def __init__(self, session: SessionType) -> None:
        self.session: SessionType = session


    async def find_all(self):
        stmt = select(User)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    

    async def create_user(
        self,
        username: str,
        password: str,
        email: str
    ) -> User:

        user = User(
            username=username,
            password=password,
            email=email
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get_by_username(
        self,
        username: str
    ) -> User | None:

        stmt = select(User).where(
            User.username == username
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
    

    async def get_by_email(self, email: str) -> User | None:

        stmt = select(User).where(
            User.email == email
        )

        result = await self.session.execute(stmt)

        user = result.scalar_one_or_none()

        return user
    

    async def get_by_email(self, email: str):

        stmt = select(User).where(
        User.email == email
    )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()