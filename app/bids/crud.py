from app.bids.models import Bid, BidInfo, BidVersion, BidStatusEnum
from app.bids.schemas import NewBidSchema, EditBidSchema

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

from uuid import UUID
from typing import Sequence


async def add_bid(db: AsyncSession, new_bid: NewBidSchema, organization_id_: UUID):
    bid_version = BidVersion(name=new_bid.name, description=new_bid.description)
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


async def update_bid_version(db: AsyncSession, bid_id: UUID, bid_info: EditBidSchema) -> Bid | None:
    bid = await db.get(Bid, bid_id, with_for_update=True)
    if not bid:
        return None
    
    prev_version = await db.get(BidVersion, bid.version_id)
    new_version = BidVersion(
        name=bid_info.name if bid_info.name else prev_version.name,
        description=bid_info.description if bid_info.description else prev_version.name,
        version=prev_version.version + 1
    )
    bid._version = new_version
    await db.commit()

    bid_info = BidInfo(bid_id=bid.id, bid_version_id=new_version.id)
    db.add(bid_info)
    await db.commit()

    return bid


async def rollback_bid_version(
    db: AsyncSession,
    bid_id: UUID,
    version: int,
) -> Bid | None:
    stmt = select(BidVersion).join(BidInfo)
    stmt = stmt.where(
        and_(BidInfo.bid_id == bid_id, BidVersion.version == version)
    )
    target_bid_version = await db.scalar(stmt)
    if not target_bid_version:
        return None
    
    bid = await db.get(Bid, bid_id, with_for_update=True)
    stmt = select(BidVersion.version).where(BidVersion.id == bid.version_id)
    now_version = await db.scalar(stmt)
    new_bid_version = BidVersion(
        name=target_bid_version.name,
        description=target_bid_version.description,
        version=now_version + 1
    )
    bid._version = new_bid_version
    await db.commit()

    bid_info = BidInfo(bid_id=bid.id, bid_version_id=new_bid_version.id)
    db.add(bid_info)
    await db.commit()

    return bid
