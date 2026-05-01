from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str