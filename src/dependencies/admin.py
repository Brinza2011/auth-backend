# from fastapi import Depends, Header, HTTPException

# from src.dependencies.jwt import get_jwt_service
# from src.service.jwt import JWTService


# async def admin_required(
#     authorization: str = Header(),
#     jwt_svc: JWTService = Depends(get_jwt_service)
# ):
#     try:
#         token = authorization.replace("Bearer ", "").strip()

#         payload = jwt_svc.decode_token(token)

#         print(payload)

#         if payload.get("role") != "admin":
#             raise HTTPException(
#                 status_code=403,
#                 detail="Access denied"
#             )
    
#         return payload

#     except Exception:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid token"
#         )