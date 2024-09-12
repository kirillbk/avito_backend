from app.employee.models import Employee

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_user(username: str, db: AsyncSession) -> Employee | None:
    stmt = select(Employee).where(Employee.username == username)
    async with db as session:
        return await session.scalar(stmt)
