from pydantic import BaseModel, EmailStr


class RegisterRequestDto(BaseModel):
    username: str
    password: str
    email: str


class UserResponseDto(BaseModel):
    id: int
    username: str
    email: str


class LoginRequestDto(BaseModel):
    password: str
    email: EmailStr


class AuthResponseDto(BaseModel):
    access_token: str
    refresh_token: str
    user: UserResponseDto
