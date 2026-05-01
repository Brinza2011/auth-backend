from src.database.db import get_session
from src.repository.user import UserRepository
from src.service.user import UserService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_svc() -> UserService:
    async for session in get_session():
        repo = UserRepository(session)
        svc = UserService(repo)
        return svc
    

async def get_user_svc() -> UserService:

    async with get_session() as session:
        repo = UserRepository(session)
        svc = UserService(repo)

        return svc