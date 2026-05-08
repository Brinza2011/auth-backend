from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from src.dependencies.jwt import get_jwt_service
from src.service.jwt import JWTPayload, JWTService
from src.exceptions.user_not_found import UserNotFoundException
from src.exceptions.user_already_exist import UserAlreadyExistsException
from src.dto.user import LoginRequestDto, RegisterRequestDto, UserResponseDto
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


@auth_router.post("/register", response_model=UserResponseDto)
async def register(
    data: RegisterRequestDto,
    svc: SignupService = Depends(get_signup_svc)
):

    try:
        user = await svc.register_user(
            username=data.username,
            password=data.password,
            email=data.email
        )

        return UserResponseDto(
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
    data: LoginRequestDto,
    svc: SignupService = Depends(get_signup_svc),
    jwt_svc: JWTService = Depends(get_jwt_service)
):
    try:
        user = await svc.login(email=data.email)

        payload: JWTPayload = {"user_id": 1, "role": "admin"}
        token = jwt_svc.encode_token(payload)
        return {
            "message": "пользователь залогинился",
            "user_id": user.id,
            "token": token
        }
    
    except UserNotFoundException as a:

        raise HTTPException(
            status_code=409,
            detail=str(a)
        )

