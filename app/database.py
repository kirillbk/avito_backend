from app.config import settings

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy import URL
from sqlalchemy.orm import DeclarativeBase

from typing import AsyncGenerator


class Base(DeclarativeBase):
    pass


db_url = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.postgres_username,
    password=settings.postgres_password,
    host=settings.postgres_host,
    port=settings.postgres_port,
    database=settings.postgres_database,
)
engine = create_async_engine(db_url, echo=settings.debug)
session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session