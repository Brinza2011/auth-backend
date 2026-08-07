from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_password: str = "12345678abcd"
    redis_url: str = f"redis://:{redis_password}@localhost:6379/0"
