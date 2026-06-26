from fastapi import APIRouter, Depends

from src.exceptions.user_dont_delete_self import DontDeleteYourSelf
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

        await svc.dont_delete_yourself(id, user.get("sub"))
        await svc.delete_user(id)
        return {
            "message": f"User {id} deleted"
        }

    except DontDeleteYourSelf as e:
        print(e)
        return{
            "message": "You can't delete yourself"
        }


