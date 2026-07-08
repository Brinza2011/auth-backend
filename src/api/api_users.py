from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.middlewares.auth import auth_required, admin_required
from src.dependencies.user import get_user_svc
from src.service.user import UserService

users_router = APIRouter()


class PaginationList[T](BaseModel):
    limit: int = 10
    offset: int = 1
    total: int = 0


class UserListDto(PaginationList):
    items: list[dict]


@users_router.get(
    "/user", dependencies=[Depends(auth_required), Depends(admin_required)]
)
async def get_users(
    service: UserService = Depends(get_user_svc), limit: int = 10, offset: int = 1
) -> UserListDto:

    if offset < 1:
        offset = 1

    if limit < 1:
        limit = 1

    users = await service.get_users(limit=limit, offset=offset)

    dtos = [
        {"id": user.id, "name": user.username, "email": user.email} for user in users
    ]
    return UserListDto(items=dtos, total=len(dtos), limit=limit, offset=offset)


# -------------------------------------------------------------------------------------------------


class ProductRepository:
    async def get_products(self):

        return [
            {"id": 1, "description": "sliva"},
            {"id": 2, "description": "perec"},
            {"id": 3, "description": "apelsin"},
            {"id": 4, "description": "kartoshka"},
            {"id": 5, "description": "ogurec"},
            {"id": 6, "description": "klubnika"},
            {"id": 7, "description": "grusha"},
            {"id": 8, "description": "vinograd"},
            {"id": 9, "description": "pomidor"},
            {"id": 10, "description": "baklajan"},
        ]


class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def get_products(self, limit: int, offset: int):
        products = await self.repo.get_products()

        return products[offset : offset + limit]


@users_router.get("/products")
async def get_items(limit: int = 10, offset: int = 1):
    repo = ProductRepository()
    service = ProductService(repo)

    return await service.get_products(limit, offset)
