from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from src.exceptions.user_already_exist import UserAlreadyExistsException
from src.dependencies.user import get_user_svc
from src.dto.user import LoginRequest, RegisterRequest, UserResponse
from src.service.sign_up import SignupService
from src.dependencies.auth import get_signup_svc

auth_router = APIRouter(prefix="/auth")


class RegisterRequestDto(BaseModel):
    email: EmailStr
    password: str


class RegisterResponseDto(BaseModel):
    access_token: str
    refresh_token: str
    user_id: int


@auth_router.post("/register", response_model=UserResponse)
async def register(
    data: RegisterRequest,
    svc: SignupService = Depends(get_signup_svc)
):

    try:
        user = await svc.register_user(
            username=data.username,
            password=data.password,
            email=data.email
        )

        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email
        )

    except UserAlreadyExistsException as e:

        raise HTTPException(
            status_code=409,
            detail=str(e)
        )



@auth_router.post("/login")
async def login(
    data: LoginRequest,
    svc: SignupService = Depends(get_signup_svc)
):

    user = await svc.login(email=data.email)

    return {
        "message": "пользователь залогинился",
        "user_id": user.id
    }
