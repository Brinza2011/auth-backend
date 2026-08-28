# from enum import Enum

# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# from src.dependencies.jwt import get_jwt_service
# from src.service.jwt import JWTService

# security = HTTPBearer()


# class UserRole(str, Enum):
#     ADMIN = "admin"
#     USER = "user"


# async def auth_required(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
#     jwt_svc: JWTService = Depends(get_jwt_service),
# ) -> None:
#     token = credentials.credentials

#     if not jwt_svc.verify_token(token):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

from enum import Enum
from typing import List, Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.cache.redis import RedisCache
from src.dependencies.ban_user import get_ban_user_service
from src.dependencies.jwt import get_jwt_service
from src.dependencies.token import get_refresh_token_repo
from src.service.ban import BanUserService
from src.service.jwt import JWTPayload, JWTService


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


security = HTTPBearer()


def require_roles(required_roles: Optional[List[Union[UserRole, str]]] = None):
    """
    Фабрика зависимостей для проверки JWT токена и ролей пользователя

    Args:
        required_roles: Список ролей, которые имеют доступ к эндпоинту.
                       Если None, то проверяется только валидность токена.

    Usage:
        @router.get("/users", dependencies=[Depends(require_roles([UserRole.ADMIN]))])
        async def get_users():
            pass

        @router.get("/profile", dependencies=[Depends(require_roles())])
        async def get_profile():
            pass
    """

    async def auth_with_roles(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        jwt_svc: JWTService = Depends(get_jwt_service),
        refresh_token_repo: RedisCache = Depends(get_refresh_token_repo),
        ban_svc: BanUserService = Depends(get_ban_user_service),
    ) -> JWTPayload:
        """
        Возвращает данные пользователя из токена для дальнейшего использования
        """
        token = credentials.credentials

        # 1. Проверяем валидность токена
        if not jwt_svc.verify_token(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 2. Получаем данные пользователя из токена
        user_data = jwt_svc.decode_token(token)  # нужно реализовать в JWTService
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        user_role = user_data.get("role")
        user_id = user_data.get("sub")

        is_banned = await ban_svc.is_banned(user_id)

        if is_banned:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User is banned"
            )

        # refresh_token = await refresh_token_repo.get(user_id)

        # if not refresh_token:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Refresh token not found"
        #     )

        # 3. Проверяем роли (если требуются)
        if required_roles:
            # Конвертируем строковые роли в Enum для сравнения
            required_roles_enum = [
                role if isinstance(role, UserRole) else UserRole(role)
                for role in required_roles
            ]

            if user_role not in [role.value for role in required_roles_enum]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. Required roles: {', '.join(required_roles_enum)}",
                )

        return {"sub": user_id, "role": user_role, **user_data}

    return auth_with_roles


auth_required = require_roles()
admin_required = require_roles([UserRole.ADMIN])
user_required = require_roles([UserRole.USER])
