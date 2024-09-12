from app.tenders.models import Tender, TenderInfo, TenderServiceTypeEnum

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from uuid import UUID


async def add_tender(
    db: AsyncSession,
    creatorId: UUID,
    organizationId: UUID,
    name: str,
    description: str,
    serviceType: TenderServiceTypeEnum
) -> Tender:
    async with db as session:
        new_tender_info = TenderInfo(name=name, description=description, serviceType=serviceType)
        session.add(new_tender_info)
        await session.commit()

        new_tender = Tender(organizationId=organizationId, creatorId=creatorId, _info=new_tender_info)
        session.add(new_tender)
        await session.commit()

    return new_tender
