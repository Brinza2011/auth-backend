from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

from src.dependencies.auth import get_signup_svc
from src.service.signup import SignupService

auth_router = APIRouter(prefix="/auth")


class RegisterRequestDto(BaseModel):
    email: EmailStr
    password: str


class RegisterResponseDto(BaseModel):
    acceess_token: str
    refresh_token: str
    user_id: int


@auth_router.post("/register")
async def register_user(
    dto: RegisterRequestDto, svc: SignupService = Depends(get_signup_svc)
) -> RegisterResponseDto:
    # TODO: Implement user registration logic
    return RegisterResponseDto(access_token="token", refresh_token="token", user_id=1)
