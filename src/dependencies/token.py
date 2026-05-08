from src.dependencies.jwt import get_jwt_service
from src.service.token import TokenService


async def get_token_service() -> TokenService:
    jwt_svc = await get_jwt_service()
    token_svc = TokenService(jwt_svc)
    return token_svc
