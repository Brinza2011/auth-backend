from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from src.exceptions.user_already_exist import UserAlreadyExistsException
from src.dependencies.token import get_token_service
from src.service.token import TokenService
from src.dependencies.jwt import get_jwt_service
from src.service.jwt import JWTPayload, JWTService
from src.exceptions.user_not_found import UserNotFoundException
from src.dto.user import LoginRequestDto, UserResponseDto
from src.service.sign_up import SignupService
from src.dependencies.auth import get_signup_svc

auth_router = APIRouter(prefix="/auth")


class RegisterRequestDto(BaseModel):
    username: str
    email: EmailStr
    password: str


class RegisterResponseDto(BaseModel):
    access_token: str
    refresh_token: str
    user_id: int


@auth_router.post("/register", response_model=UserResponseDto)
async def register(
    data: RegisterRequestDto,
    svc: SignupService = Depends(get_signup_svc),
    token_svc: TokenService = Depends(get_token_service)
):

    try:
                
        payload: JWTPayload = {"sub": 1, "role": "admin"}
        access_token = token_svc.access_token(payload) 
        refresh_token = token_svc.refresh_token(payload)

        user = await svc.register_user(
            username=data.username,
            password=data.password,
            email=data.email
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user
        }

    except UserAlreadyExistsException as e:

        raise HTTPException(
            status_code=409,
            detail=str(e)
        )



@auth_router.post("/login")
async def login(
    data: LoginRequestDto,
    svc: SignupService = Depends(get_signup_svc),
    jwt_svc: JWTService = Depends(get_jwt_service),
    token_svc: TokenService = Depends(get_token_service)
):
    try:
        user = await svc.login(email=data.email)


        if user.password != data.password:
            raise HTTPException(
                status_code=401,
                detail="Неправильный пароль"
            )

        payload: JWTPayload = {
            "sub": user.id,
            "role": "admin"
        }

        access_token = token_svc.access_token(payload)
        refresh_token = token_svc.refresh_token(payload)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user
        }

    except UserNotFoundException as a:

        raise HTTPException(
            status_code=409,
            detail=str(a)
        )
