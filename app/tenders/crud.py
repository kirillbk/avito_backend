from app.tenders.models import (
    Tender,
    TenderVersion,
    TenderServiceTypeEnum,
    TenderInfo,
    TenderStatusEnum,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
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
    tender_version = TenderVersion(
        name=name, description=description, serviceType=serviceType
    )
    db.add(tender_version)
    await db.commit()

    tender = Tender(
        organizationId=organizationId, creatorId=creatorId, _version=tender_version
    )
    db.add(tender)
    await db.commit()

    tender_info = TenderInfo(tender_id=tender.id, tender_version_id=tender_version.id)
    db.add(tender_info)
    await db.commit()

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

    return (await db.scalars(stmt)).all()


async def get_tenders_by_user(
    db: AsyncSession, limit: int, offset: int, creator_id: UUID
) -> Sequence[Tender]:
    stmt = (
        select(Tender)
        .where(Tender.creatorId == creator_id)
        .options(joinedload(Tender._version))
    )
    stmt = stmt.limit(limit).offset(offset)

    return (await db.scalars(stmt)).all()


async def update_tender_status(
    db: AsyncSession, tender_id: UUID, status: TenderStatusEnum
) -> Tender | None:
    stmt = select(Tender).where(Tender.id == tender_id).with_for_update()
    tender = await db.scalar(stmt)
    if not tender:
        return None

    tender.status = status
    await db.commit()
    tender._version = await db.get(TenderVersion, tender.version_id)

    return tender


async def get_tender_status(
    db: AsyncSession, tender_id: UUID
) -> TenderStatusEnum | None:
    stmt = select(Tender.status).where(Tender.id == tender_id)
    return await db.scalar(stmt)


async def get_tender_organization_id(db: AsyncSession, tender_id: UUID) -> UUID | None:
    stmt = select(Tender.organizationId).where(Tender.id == tender_id)
    return await db.scalar(stmt)


async def get_tender(db: AsyncSession, tender_id: UUID) -> Tender | None:
    return await db.get(Tender, tender_id)


async def update_tender_version(
    db: AsyncSession,
    tender_id: UUID,
    name: str | None,
    description: str | None,
    serviceType: TenderServiceTypeEnum | None,
) -> Tender:
    stmt = select(Tender).where(Tender.id == tender_id).with_for_update()
    tender = await db.scalar(stmt)

    old_tender_version = await db.get(TenderVersion, tender.version_id)
    new_tender_version = TenderVersion(
        name=name if name else old_tender_version.name,
        description=description if description else old_tender_version.description,
        serviceType=serviceType if serviceType else old_tender_version.serviceType,
        version=old_tender_version.version + 1,
    )
    db.add(new_tender_version)
    await db.commit()

    tender._version = new_tender_version
    await db.commit()

    tender_info = TenderInfo(
        tender_id=tender_id, tender_version_id=new_tender_version.id
    )
    db.add(tender_info)
    await db.commit()

    return tender


async def rollback_tender_version(
    db: AsyncSession,
    tender_id: UUID,
    version: int,
) -> Tender | None:
    stmt = select(TenderVersion).join(TenderInfo)
    stmt = stmt.where(
        and_(TenderInfo.tender_id == tender_id, TenderVersion.version == version)
    )
    source_tender_version = await db.scalar(stmt)
    if not source_tender_version:
        return None

    stmt = select(Tender).where(Tender.id == tender_id).with_for_update()
    tender = await db.scalar(stmt)

    stmt = select(TenderVersion.version).where(TenderVersion.id == tender.version_id)
    current_version = await db.scalar(stmt)
    new_tender_version = TenderVersion(
        name=source_tender_version.name,
        description=source_tender_version.description,
        serviceType=source_tender_version.serviceType,
        version=current_version + 1,
    )
    db.add(new_tender_version)
    await db.commit()

    tender._version = new_tender_version
    await db.commit()

    tender_info = TenderInfo(
        tender_id=tender_id, tender_version_id=new_tender_version.id
    )
    db.add(tender_info)
    await db.commit()

    return tender
