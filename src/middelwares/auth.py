from fastapi import Request


async def auth_middleware(request: Request) -> None:

    print(request.base_url)
