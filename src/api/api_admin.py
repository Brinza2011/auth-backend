from fastapi import APIRouter, Depends

from src.middlewares.current_user import get_current_user
from src.service.jwt import JWTPayload
from src.middlewares.auth import admin_required
from src.dependencies.auth import get_signup_svc
from src.service.signup import SignupService


admin_router = APIRouter(prefix="/auth")


@admin_router.delete("/api/v1/admin/users/{id}", dependencies=[Depends(admin_required)])
async def delete_user(
    id: str,
    svc: SignupService = Depends(get_signup_svc),
    user: JWTPayload = Depends(get_current_user)
):
    
    try:
        await svc.dont_delete_yourself(id, user)
        await svc.delete_user(id)
        return {
            "message": f"User {id} deleted"
        }

    except:
        return{
            "message": "You can't delete yourself"
        }


@admin_router.get("/test")
async def test(
    id: str,
    user: JWTPayload = Depends(get_current_user)
):
    print(type(user.get("sub")))
    print(user.get("sub") == id)

    if user.get("sub") == id:
        return{"You can't delete yourself"}

    return user
