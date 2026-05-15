
from src.service.token import TokenService
from src.dependencies.jwt import get_jwt_service


async def get_token_service() -> TokenService:
    jwt_svc = await get_jwt_service()
    token_svc = TokenService(jwt_svc)
    return token_svc
