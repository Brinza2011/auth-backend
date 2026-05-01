from src.database.db import get_session
from src.repository.user import UserRepository
from src.service.user import UserService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_svc(
    session: AsyncSession = Depends(get_session)
) -> UserService:
    """FastAPI dependency для UserService"""

    repo = UserRepository(session)
    svc = UserService(repo)

    return svc