from fastapi import Depends, HTTPException, Header, Request
from src.dependencies.jwt import get_jwt_service
from src.service.jwt import JWTService


async def auth_middleware(request: Request) -> None:
    print(request.base_url)


# async def auth_required(
#     request: Request,    
#     x_role: str = Header(),
#     svc: JWTService = Depends(get_jwt_service)
# ) -> None:
    
#     authorization = request.headers.get("Authorization")
#     print(authorization)

#     if not authorization:
#         raise HTTPException(status_code=401, detail="Authorization header missing")

#     x_role_modify = x_role.strip().upper()

#     if x_role_modify != "ADMIN":
#         raise HTTPException(
#             status_code=403,
#             detail="Access denied"
#         )
    

async def auth_required(
    authorization: str = Header(),
    jwt_svc: JWTService = Depends(get_jwt_service)
):
    print(authorization)
    token = authorization.replace("Bearer", " ").strip() #не трогать пробел
    print(token)

    try:
        payload = jwt_svc.decode_token(token)

        print(payload)

        return payload

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
