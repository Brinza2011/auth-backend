from fastapi import APIRouter
from src.api.api_ban import ban_router
from src.api.api_admin import admin_router
from src.api.api_auth import auth_router
from src.api.api_users import users_router

router = APIRouter(prefix="/api")

router.include_router(users_router, prefix="/v1")
router.include_router(auth_router, prefix="/v1")
router.include_router(admin_router, prefix="/v1")
router.include_router(ban_router, prefix="/v1")
