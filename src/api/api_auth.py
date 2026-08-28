import re

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator

from src.dependencies.auth import get_signup_svc
from src.dependencies.jwt import get_jwt_service
from src.dependencies.token import get_refresh_token_repo, get_token_service
from src.dto.user import AuthResponseDto, LoginRequestDto, UserResponseDto
from src.exceptions.user_already_exist import UserAlreadyExistsException
from src.exceptions.user_not_found import UserNotFoundException
from src.middlewares.current_user import get_current_user
from src.repository.refresh_token import RefreshTokenRepository
from src.service.jwt import JWTPayload, JWTService
from src.service.sign_up import SignupService
from src.service.token import TokenService

auth_router = APIRouter(prefix="/auth")


class RegisterRequestDto(BaseModel):
    username: str = Field(min_length=5, max_length=30)
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(_cls, value: str):

        # минимум 2 заглавные буквы
        uppercases = re.findall(r"[A-Z]", value)

        if len(uppercases) < 2:
            raise ValueError("Password must contain at least 2 uppercase letters")

        # минимум 1 цифра
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least 1 number")

        # минимум 1 буква
        if not re.search(r"[a-zA-Z]", value):
            raise ValueError("Password must contain letters")

        return value


class RegisterResponseDto(BaseModel):
    access_token: str
    refresh_token: str
    user_id: int


@auth_router.post("/register", response_model=AuthResponseDto)
async def register(
    data: RegisterRequestDto,
    svc: SignupService = Depends(get_signup_svc),
    token_svc: TokenService = Depends(get_token_service),
    jwt_svc: JWTService = Depends(get_jwt_service),
):

    try:
        user = await svc.register_user(
            username=data.username, password=data.password, email=data.email
        )

        payload: JWTPayload = {"sub": str(user.id), "role": user.role}
        access_token = token_svc.access_token(payload)
        refresh_token = token_svc.refresh_token(payload)

        a = jwt_svc.encode_token(payload)

        print(jwt_svc.decode_token(a))

        return AuthResponseDto(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponseDto(id=user.id, username=user.username, email=user.email),
        )

    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))


@auth_router.post("/login")
async def login(
    data: LoginRequestDto,
    svc: SignupService = Depends(get_signup_svc),
    jwt_svc: JWTService = Depends(get_jwt_service),
    token_svc: TokenService = Depends(get_token_service),
):
    try:
        user = await svc.login(email=data.email)

        if user.password != data.password:
            raise HTTPException(status_code=401, detail="Неправильный пароль")

        payload: JWTPayload = {"sub": user.id, "role": user.role, "exp": 30}

        a = jwt_svc.encode_token(payload)

        access_token = token_svc.access_token(payload)
        refresh_token = token_svc.refresh_token(payload)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user,
        }

    except UserNotFoundException as a:
        raise HTTPException(status_code=409, detail=str(a))


class RefreshRequestDto(BaseModel):
    refresh_token: str


@auth_router.post("/refresh")
async def refresh(
    data: RefreshRequestDto,
    token_svc: TokenService = Depends(get_token_service),
    user: JWTPayload = Depends(get_current_user),
    refresh_token_repo: RefreshTokenRepository = Depends(get_refresh_token_repo),
):
    refresh_token = await refresh_token_repo.get(str(user["sub"]))
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if refresh_token["token"] != data.refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    await refresh_token_repo.delete(user["sub"])

    payload: JWTPayload = {
        "sub": user["sub"],
        "role": user["role"],
    }
    access_token = token_svc.access_token(payload)
    refresh_token = token_svc.refresh_token(payload)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
