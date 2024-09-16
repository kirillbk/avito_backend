from app.main import app, lifespan
from app.database import engine, get_db

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from typing import AsyncGenerator


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="function")
async def db_test_session() -> AsyncGenerator[AsyncConnection, None]:
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
async def aclient(db_test_session) -> AsyncGenerator[AsyncClient, None]:
    """
    Асинхронный клиент
    """
    app.dependency_overrides[get_db] = lambda: db_test_session

    async with lifespan(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            yield ac

@pytest.fixture()
def tasks_db(tmpdir):
    """Подключение к БД перед тестами, отключение после."""
    # Setup : start db
    tasks.start_tasks_db(str(tmpdir), 'tiny')
    yield  # здесь происходит тестирование
    # Teardown : stop db
    tasks.stop_tasks_db()

# @pytest.fixture(scope="session")
# def users() -> tuple[dict[str, str]]:
#     return (
#         dict(
#             login="user1@example.com",
#             password="password1",
#             project_id="1fa85f64-5717-4562-b3fc-2c963f66afa2",
#             env="prod",
#             domain="canary",
#         ),
#         dict(
#             login="user2@example.com",
#             password="password2",
#             project_id="3fa85f64-5717-4562-b3fc-2c963f66afa3",
#             env="prod",
#             domain="canary",
#         ),
#         dict(
#             login="user3@example.com",
#             password="password3",
#             project_id="3fa85f64-5717-4562-b3fc-2c963f66afa3",
#             env="prod",
#             domain="canary",
#         ),
#     )
