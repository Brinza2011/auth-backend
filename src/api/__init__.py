

from fastapi import APIRouter
from src.api.api_users import users_router


router = APIRouter(prefix="/api")

router.include_router(users_router, prefix="/v1")