from app.tenders.models import Tender, TenderInfo, TenderServiceTypeEnum

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from uuid import UUID
from typing import Sequence


async def add_tender(
    db: AsyncSession,
    creatorId: UUID,
    organizationId: UUID,
    name: str,
    description: str,
    serviceType: TenderServiceTypeEnum,
) -> Tender:
    async with db as session:
        new_tender_info = TenderInfo(
            name=name, description=description, serviceType=serviceType
        )
        session.add(new_tender_info)
        await session.commit()

        new_tender = Tender(
            organizationId=organizationId, creatorId=creatorId, _info=new_tender_info
        )
        session.add(new_tender)
        await session.commit()

    return new_tender


async def get_tenders_by_type(
    db: AsyncSession,
    limit: int,
    offset: int,
    service_type: TenderServiceTypeEnum | None = None,
) -> Sequence[Tender]:
    stmt = select(Tender).join(TenderInfo)
    if service_type:
        stmt = stmt.where(TenderInfo.serviceType == service_type)
    stmt = stmt.limit(limit).offset(offset)

    async with db as session:
        return (await session.scalars(stmt)).all()


async def get_tenders_by_user(
    db: AsyncSession, limit: int, offset: int, creator_id: UUID
) -> Sequence[Tender]:
    stmt = select(Tender).where(Tender.creatorId == creator_id)
    stmt = stmt.limit(limit).offset(offset)

    async with db as session:
        return (await session.scalars(stmt)).all()
