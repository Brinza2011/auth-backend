from sqlalchemy import Column, Integer, String

from src.database.db import Base


from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role: Mapped[str] = mapped_column(default="USER")
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]

    def __str__(self) -> str:
        return f"{self.username}"
