from fastapi import Depends
from src.exceptions.user_dont_delete_self import DontDeleteYourSelf
from src.middlewares.current_user import get_current_user
from src.service.jwt import JWTPayload
from src.exceptions.user_not_found import UserNotFoundException
from src.exceptions.user_already_exist import UserAlreadyExistsException
from src.models.user import UserModel
from src.repository.user import UserRepository


class SignupService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def register_user(
        self, username: str, password: str, email: str
    ) -> UserModel:

        existing_email = await self.repo.get_by_email(email)

        if existing_email:
            raise UserAlreadyExistsException("User with this email already exists")

        existing_username = await self.repo.get_by_username(username)

        if existing_username:
            raise UserAlreadyExistsException("User with this username already exists")

        # Создаём пользователя
        user = await self.repo.create_user(username, password, email)

        return user

    async def login(self, email: str):

        user = await self.repo.get_by_email(email)

        if not user:
            raise UserNotFoundException("User not found")

        return user

    async def delete_user(self, user_id: int) -> None:
        await self.repo.delete_user(user_id)

    async def dont_delete_yourself(self, id: str, sub: str) -> None:

        if sub == id:
            raise DontDeleteYourSelf("You can't delete yourself")
