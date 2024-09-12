from app.organization.models import Organization, OrganizationResponsible

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from uuid import UUID


async def get_responsible(user_id: UUID, organization_id: UUID, db: AsyncSession) -> OrganizationResponsible | None:
    stmt = select(OrganizationResponsible)
    stmt = stmt.where(
        and_(
            user_id == OrganizationResponsible.user_id,
            organization_id == OrganizationResponsible.organization_id
        )
    )
    async with db as session:
        return await session.scalar(stmt)
