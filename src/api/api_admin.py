from fastapi import APIRouter, Depends

from src.middlewares.current_user import get_current_user
from src.service.jwt import JWTPayload
from src.middlewares.auth import admin_required
from src.dependencies.auth import get_signup_svc
from src.service.signup import SignupService


admin_router = APIRouter(prefix="/auth")


@admin_router.delete("/api/v1/admin/users/{id}", dependencies=[Depends(admin_required)])
async def delete_user(
    id: int,
    svc: SignupService = Depends(get_signup_svc)
):
    await svc.delete_user(id)

    return {
        "message": f"User {id} deleted"
    }

@admin_router.get("/test")
async def test(
    user: JWTPayload = Depends(get_current_user)
):
    if user.get("sub") == id:
        return{"You can't delete yourself"}
    
    return user