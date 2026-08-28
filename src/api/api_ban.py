from fastapi import APIRouter, Depends

from src.dependencies.ban_user import get_ban_user_service
from src.service.ban import BanUserService


ban_router = APIRouter()


@ban_router.post("/ban")
async def ban_user(
    user_id: int, ban_user_svc: BanUserService = Depends(get_ban_user_service)
):

    await ban_user_svc.ban_user(user_id)

    return {"message": f"User {user_id} has been banned"}
