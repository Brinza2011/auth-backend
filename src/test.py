import asyncio

from src.dependencies.jwt import get_jwt_service
from src.dependencies.token import get_token_service
from src.service.jwt import JWTPayload, JWTService


async def main():
    # token_svc: JWTService = await get_jwt_service()

    # payload: JWTPayload = {"sub": "1", "role": "admin", "exp": 5}
    # token = token_svc.encode_token(payload)

    # print(token)

    # decoded_payload = token_svc.decode_token(token)
    # print(decoded_payload)
    jwt_svc = await get_jwt_service()
    token_svc = await get_token_service()
    payload: JWTPayload = {"sub": "1", "role": "admin", "exp": None}

    access_token = token_svc.access_token(payload)  # 5 minutes
    refresh_token = token_svc.refresh_token(payload)  # 15 minutes

    print(access_token)
    print(refresh_token)

    print(jwt_svc.decode_token(access_token))


if __name__ == "__main__":
    asyncio.run(main())


def test_a():
    print("Hello")

    if True:
        pass

    print("HHHHHHH")


def test_b() -> int:
    return "Hello world !"
