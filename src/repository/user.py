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