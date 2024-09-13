from app.bids.models import Bid, BidInfo, BidVersion
from app.bids.schemas import NewBidSchema

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from uuid import UUID
from typing import Sequence


async def add_bid(db: AsyncSession, new_bid: NewBidSchema):
    bid_version = BidVersion(name=new_bid.name, description=new_bid.description)
    db.add(bid_version)
    await db.commit()

    bid = Bid(
        tenderId=new_bid.tenderId,
        authorId=new_bid.authorId,
        authorType=new_bid.authorType,
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
