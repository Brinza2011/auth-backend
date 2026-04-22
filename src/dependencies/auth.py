from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_session
from src.repository.user import UserRepository
from src.service.signup import SignupService


async def get_signup_svc(session: AsyncSession = Depends(get_session)) -> SignupService:
    """FastAPI dependency для UserService"""

    repo = UserRepository(session)
    svc = SignupService(repo)

    return svc
