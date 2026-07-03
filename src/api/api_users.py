from ast import arg

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.dependencies.user import get_user_svc
from src.middlewares.auth import admin_required, auth_required
from src.service.user import UserService

users_router = APIRouter()

# limit/size - сколько мы отображаем пользователей на одной список/странице
# offset/page - смещение от начала списка/страницы


class PagginationList[T](BaseModel):
    items: T
    limit: int = 10
    offset: int = 1
    total: int = 0


class UserListDto(PagginationList[list[dict]]):
    items: list[dict]


@users_router.get(
    "/user", dependencies=[Depends(auth_required), Depends(admin_required)]
)
async def get_users(
    service: UserService = Depends(get_user_svc), limit: int = 10, offset: int = 1
) -> UserListDto:

    if offset < 1:
        offset = 1

    if limit < 1:
        limit = 1

    users = await service.get_users(limit=limit, offset=offset)
    dtos = [
        {"id": user.id, "name": user.username, "email": user.email} for user in users
    ]
    return UserListDto(items=dtos, total=len(dtos), limit=limit, offset=offset)
