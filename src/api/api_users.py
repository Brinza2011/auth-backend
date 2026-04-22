from fastapi import APIRouter, Depends

from src.dependencies.user import get_user_svc
from src.service.user import UserService

users_router = APIRouter()

@users_router.get("/user")
async def get_users(service: UserService = Depends(get_user_svc)):
    users = await service.get_users()

    return [
        {
            "id": user.id,
            "name": user.username
        }
        for user in users
    ]