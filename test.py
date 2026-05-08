import asyncio

from src.dependencies.jwt import get_jwt_service
from src.service.jwt import JWTPayload, JWTService


async def main():
    token_svc: JWTService = await get_jwt_service()

    payload: JWTPayload = {"user_id": 1, "role": "admin"}
    token = token_svc.encode_token(payload)

    print(token)

    decoded_payload = token_svc.decode_token(token)
    print(decoded_payload)


if __name__ == "__main__":
    asyncio.run(main())
