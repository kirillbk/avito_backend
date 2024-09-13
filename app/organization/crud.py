from app.organization.models import OrganizationResponsible

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from uuid import UUID


async def get_responsible_id(
    db: AsyncSession, user_id: UUID, organization_id: UUID
) -> UUID | None:
    stmt = select(OrganizationResponsible.id)
    stmt = stmt.where(
        and_(
            user_id == OrganizationResponsible.user_id,
            organization_id == OrganizationResponsible.organization_id,
        )
    )
    return await db.scalar(stmt)


async def get_user_organization_id(db: AsyncSession, user_id: UUID) -> UUID | None:
    stmt = select(OrganizationResponsible.organization_id)
    stmt = stmt.where(OrganizationResponsible.user_id == user_id)
    return await db.scalar(stmt)


async def get_responsible(
    db: AsyncSession, user_id: UUID, organization_id: UUID
) -> OrganizationResponsible | None:
    stmt = select(OrganizationResponsible)
    stmt = stmt.where(
        and_(
            user_id == OrganizationResponsible.user_id,
            organization_id == OrganizationResponsible.organization_id,
        )
    )
    return await db.scalar(stmt)
