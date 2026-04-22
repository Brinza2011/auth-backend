import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session


DATABASE_URL = "sqlite+aiosqlite:///./users.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)

SessionType = Session


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()



async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

if __name__ == "__main__":
    asyncio.run(init_db())