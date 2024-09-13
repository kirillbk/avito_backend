from app.employee.models import Employee

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from uuid import UUID


async def get_user_id(db: AsyncSession, username: str) -> UUID | None:
    stmt = select(Employee.id).where(Employee.username == username)
    return await db.scalar(stmt)


async def get_user(db: AsyncSession, id: UUID) -> Employee | None:
    return await db.get(Employee, id)
