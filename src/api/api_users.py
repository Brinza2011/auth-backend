from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.cache.redis import RedisCache
from src.dependencies.cache import get_cache
from src.dependencies.user import get_user_svc
from src.ratelimiter.ratelimiter import RateLimiter, rate_limiter
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
    "/user",
    # dependencies=[Depends(auth_required), Depends(admin_required)] make this import
)
@rate_limiter(window = "1 minute", requests = 10)
async def get_users(
    user_id: str = "5",
    service: UserService = Depends(get_user_svc),
    cache: RedisCache = Depends(get_cache),
    limit: int = 1000,
    offset: int = 1,
) -> UserListDto:

    key = f"users_{offset}_{limit}"

    users_cache = cache.get(key)
    if users_cache:
        return UserListDto(
            items=users_cache,
            total=len(users_cache),
            limit=limit,
            offset=offset,
        )

    users = await service.get_users(limit=limit, offset=offset)

    dtos = [
        {
            "id": user.id,
            "name": user.username,
            "email": user.email,
        }
        for user in users
    ]

    cache.set(key, dtos, ex=300)  # кэш на 5 минут

    return UserListDto(
        items=dtos,
        total=len(dtos),
        limit=limit,
        offset=offset,
    )

@users_router.get(
    "/userrr",
    dependencies=[Depends(RateLimiter("minute", 10))]
)

async def get_users():
    return {"message": "OK"}
