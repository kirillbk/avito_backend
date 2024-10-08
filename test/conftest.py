from app.main import app, lifespan
from app.database import engine, get_db

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from typing import AsyncGenerator


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="function")
async def db_test() -> AsyncGenerator[AsyncSession, None]:
    """
    Откат изменений БД после каждого теста
    """
    connection = await engine.connect()
    transaction = await connection.begin()
    session = AsyncSession(bind=connection, expire_on_commit=False)

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest.fixture(scope="function")
async def aclient(db_test) -> AsyncGenerator[AsyncClient, None]:
    """
    Асинхронный клиент
    """
    app.dependency_overrides[get_db] = lambda: db_test

    async with lifespan(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            yield ac


@pytest.fixture
def new_tender() -> dict[str, str]:
    return {
        "name": "Тендер 1",
        "description": "Описание тендера",
        "serviceType": "Construction",
        "status": "Open",
        "organizationId": "550e8400-e29b-41d4-a716-446655440000",
        "creatorUsername": "user",
    }


@pytest.fixture
def new_bid() -> dict[str, str]:
    return {
        "name": "new bid",
        "description": "new bid descrition",
        "tenderId": "550e8400-e29b-41d4-a716-446655440000",
        "authorType": "Organization",
        "authorId": "550e8400-e29b-41d4-a716-446655440000",
    }
