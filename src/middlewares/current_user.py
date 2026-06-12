from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.dependencies.jwt import get_jwt_service
from src.service.jwt import JWTPayload, JWTService

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_svc: JWTService = Depends(get_jwt_service),
) -> JWTPayload:
    user = jwt_svc.decode_token(credentials.credentials)
    return user
