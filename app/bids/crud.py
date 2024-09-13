from app.bids.models import Bid, BidInfo, BidVersion, BidStatusEnum
from app.bids.schemas import NewBidSchema

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from uuid import UUID
from typing import Sequence


async def add_bid(db: AsyncSession, new_bid: NewBidSchema, organization_id_: UUID):
    bid_version = BidVersion(name=new_bid.name, description=new_bid.description)
    db.add(bid_version)
    await db.commit()

    bid = Bid(
        tenderId=new_bid.tenderId,
        authorId=new_bid.authorId,
        authorType=new_bid.authorType,
        organization_id=organization_id_,
        version_id=bid_version.id,
        _version=bid_version,
    )
    db.add(bid)
    await db.commit()

    bid_info = BidInfo(bid_id=bid.id, bid_version_id=bid_version.id)
    db.add(bid_info)
    await db.commit()

    return bid


async def get_bids_by_user(
    db: AsyncSession, limit: int, offset: int, user_id: UUID
) -> Sequence[Bid]:
    stmt = select(Bid).where(Bid.authorId == user_id)
    stmt = stmt.limit(limit).offset(offset)
    stmt = stmt.options(joinedload(Bid._version))

    return (await db.scalars(stmt)).all()


async def get_bids_by_tender(
    db: AsyncSession, limit: int, offset: int, tender_id: UUID
) -> Sequence[Bid]:
    stmt = select(Bid).where(Bid.tenderId == tender_id)
    stmt = stmt.limit(limit).offset(offset)
    stmt = stmt.options(joinedload(Bid._version))

    return (await db.scalars(stmt)).all()


async def get_bid(db: AsyncSession, id: UUID) -> Bid | None:
    return await db.get(Bid, id, options=[joinedload(Bid._version)])


async def update_bid_status(db: AsyncSession, bid_id: UUID, status: BidStatusEnum) -> Bid | None:
    bid = await db.get(Bid, bid_id, options=[joinedload(Bid._version)])
    if not bid:
        return None
    bid.status = status
    await db.commit()

    return bid