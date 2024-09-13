from app.organization.models import Organization, OrganizationResponsible

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from uuid import UUID


async def get_responsible_id(db: AsyncSession, user_id: UUID, organization_id: UUID) -> UUID | None:
    stmt = select(OrganizationResponsible.id)
    stmt = stmt.where(
        and_(
            user_id == OrganizationResponsible.user_id,
            organization_id == OrganizationResponsible.organization_id
        )
    )
    return await db.scalar(stmt)
