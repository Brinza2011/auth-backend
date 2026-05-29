
from fastapi import HTTPException, Header, Request


async def auth_middleware(request: Request) -> None:

    print(request.base_url)


async def admin_required(
    x_role: str = Header()
):
    x_role_modify = x_role.strip().upper()

    if x_role_modify != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )
