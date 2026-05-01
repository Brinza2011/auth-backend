from src.config.auth_config import JWT_ALGORITHM, JWT_SECRET_KEY
from src.service.jwt import JWTService


async def get_jwt_service():
    return JWTService(secret_key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
