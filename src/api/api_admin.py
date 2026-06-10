from fastapi import APIRouter, Depends

from src.dependencies.user import get_user_svc
from src.middlewares.auth import require_admin
from src.middlewares.current_user import get_current_user
from src.service.jwt import JWTPayload
from src.service.user import UserService

admin_router = APIRouter(prefix="/admin")


@admin_router.get("/users", dependencies=[Depends(require_admin)])
async def get_users(service: UserService = Depends(get_user_svc)):
    users = await service.get_users()

    return [
        {"id": user.id, "name": user.username, "email": user.email} for user in users
    ]


@admin_router.get("/test")
async def test(user: JWTPayload = Depends(get_current_user)):
    if user.get("sub") == id:
        return {"message": "Ты не можешь себя удалить"}

    return user
