from src.service.sign_up import SignupService
from src.database.db import get_session
from src.repository.user import UserRepository
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_signup_svc(session: AsyncSession = Depends(get_session)) -> SignupService:
    """FastAPI dependency для UserService"""

    repo = UserRepository(session)
    svc = SignupService(repo)

    return svc
