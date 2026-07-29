import json
from fastapi import APIRouter, Depends
from src.cache import redis
from src.cache.redis import RedisCache, redis_cache
from src.dependencies.cache import get_cache
from src.dependencies.user import get_user_svc
from src.exceptions.user_dont_delete_self import DontDeleteYourSelf
from src.middlewares.current_user import get_current_user
from src.service.jwt import JWTPayload
from src.middlewares.auth import admin_required
from src.dependencies.auth import get_signup_svc
from src.service.sign_up import SignupService
from src.service.user import UserService


admin_router = APIRouter(prefix="/auth")


@admin_router.delete("/api/v1/admin/users/{id}", dependencies=[Depends(admin_required)])
async def delete_user(
    id: str,
    svc: SignupService = Depends(get_signup_svc),
    user: JWTPayload = Depends(get_current_user),
):

    try:
        await svc.dont_delete_yourself(id, user.get("sub"))
        await svc.delete_user(int(id))
        return {"message": f"User {id} deleted"}

    except DontDeleteYourSelf as e:
        print(e)
        return {"message": "You can't delete yourself"}


@admin_router.get("/users/admin")
async def get_admin_users(
    svc: UserService = Depends(get_user_svc),
    cache: RedisCache = Depends(get_cache)
):
    cache = redis_cache.get("admin_users")
    if cache:
        return json.loads(cache)

    users = await svc.repo.find_all()

    admins = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        }
        for user in users
        if user.role == "ADMIN"
    ]

    redis_cache.set(
        "admin_users",
        admins,
        ex=60,
    )

    return admins