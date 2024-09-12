from app.tenders.models import Tender, TenderVersion, TenderServiceTypeEnum, TenderInfo

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

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
        tender_version = TenderVersion(
            name=name, description=description, serviceType=serviceType
        )
        session.add(tender_version)
        await session.commit()

        tender = Tender(
            organizationId=organizationId, creatorId=creatorId, _version=tender_version
        )
        session.add(tender)
        await session.commit()

        tender_info = TenderInfo(
            tender_id=tender.id, tender_version_id=tender_version.id
        )
        session.add(tender_info)
        await session.commit()

    return tender


async def get_tenders_by_type(
    db: AsyncSession,
    limit: int,
    offset: int,
    service_type: TenderServiceTypeEnum | None = None,
) -> Sequence[Tender]:
    stmt = select(Tender).join(TenderVersion).options(joinedload(Tender._version))
    if service_type:
        stmt = stmt.where(TenderVersion.serviceType == service_type)
    stmt = stmt.limit(limit).offset(offset)

    async with db as session:
        return (await session.scalars(stmt)).all()


async def get_tenders_by_user(
    db: AsyncSession, limit: int, offset: int, creator_id: UUID
) -> Sequence[Tender]:
    stmt = (
        select(Tender)
        .where(Tender.creatorId == creator_id)
        .options(joinedload(Tender._version))
    )
    stmt = stmt.limit(limit).offset(offset)

    async with db as session:
        return (await session.scalars(stmt)).all()


async def get_tender(db: AsyncSession, tender_id: UUID) -> Tender:
    async with db as session:
        return await session.get(Tender, tender_id)


async def update_tender(
    db: AsyncSession,
    tender_id: UUID,
    name: str | None,
    description: str | None,
    serviceType: TenderServiceTypeEnum | None
) -> Tender:
    async with db as session:
        stmt = select(Tender).where(Tender.id == tender_id).with_for_update()
        tender = await session.scalar(stmt)
        old_tender_version = await session.get(TenderVersion, tender.version_id)
        new_tender_version = TenderVersion(
            name=name if name else old_tender_version.name,
            description=description if description else old_tender_version.description,
            serviceType=serviceType if serviceType else old_tender_version.serviceType,
            version = old_tender_version.version + 1   
        )
        session.add(new_tender_version)
        await session.commit()

        tender._version = new_tender_version
        await session.commit()

        tender_info = TenderInfo(tender_id=tender_id, tender_version_id=new_tender_version.id)
        session.add(tender_info)
        await session.commit()

    return tender
