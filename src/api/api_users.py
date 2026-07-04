from ast import arg

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.dependencies.user import get_user_svc
from src.middlewares.auth import admin_required, auth_required
from src.service.user import UserService

users_router = APIRouter()

# limit/size - сколько мы отображаем пользователей на одной список/странице
# offset/page - смещение от начала списка/страницы


class PagginationList[T](BaseModel):
    items: T
    limit: int = 10
    offset: int = 1
    total: int = 0


class UserListDto(PagginationList[list[dict]]):
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


# -------------------------------------

class ProductRepository:
    def __init__(self, product: list[dict]):
        self.product = product

        product = [
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

    async def product_repo(limit: int = 10, offset: int = 1, product: str) :
        ovoshi = product[offset : offset + limit]
        return ovoshi


class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo


    async def get_product_service(self,limit: int = 10, offset: int = 1):
        return await self.repo.product_repo(limit, offset)


@users_router.get("/products")
async def get_items(limit: int = 10, offset: int = 1):

    product = [
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

    ovoshi = product[offset : offset + limit]

    return ovoshi
