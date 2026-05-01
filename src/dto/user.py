from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class LoginRequest(BaseModel):
    email: EmailStr