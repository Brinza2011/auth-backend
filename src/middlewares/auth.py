# from fastapi import Depends, Header, HTTPException

# from src.dependencies.jwt import get_jwt_service
# from src.service.jwt import JWTService


# async def auth_required(
#     authorization: str = Header(), jwt_svc: JWTService = Depends(get_jwt_service)
# ) -> None:

#     token = authorization.replace("Bearer", " ").strip()  # не трогать пробел

#     is_valid = jwt_svc.verify_token(token)
#     if not is_valid:
#         raise HTTPException(status_code=401, detail="Invalid token")


from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.dependencies.jwt import get_jwt_service
from src.service.jwt import JWTService

security = HTTPBearer()


async def auth_required(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_svc: JWTService = Depends(get_jwt_service),
) -> None:
    token = credentials.credentials

    if not jwt_svc.verify_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
