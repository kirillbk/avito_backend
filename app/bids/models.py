from app.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import String, Enum, ForeignKey, CheckConstraint

from uuid import UUID
from datetime import datetime
import enum


class BidStatusEnum(str, enum.Enum):
    CREATED = "Created"
    PUBLISHED = "Published"
    CANCELED = "Canceled"


class BidAuthorTypeEnum(str, enum.Enum):
    ORGANIZATION = "Organization"
    USER = "User"


class Bid(Base):
    __tablename__ = "bid"

    id: Mapped[UUID] = mapped_column(server_default=func.gen_random_uuid(), primary_key=True)

    tenderId: Mapped[UUID] = mapped_column(ForeignKey("tender.id",ondelete="CASCADE"), nullable=False)
    authorId: Mapped[UUID] = mapped_column(ForeignKey("employee.id",ondelete="CASCADE"), nullable=False)
   
    # name
    # description
    # version
    status: Mapped[BidStatusEnum] = mapped_column(Enum(BidStatusEnum), nullable=False)
    authorType: Mapped[BidAuthorTypeEnum] = mapped_column(Enum(BidAuthorTypeEnum), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())


class BidInfo(Base):
    __tablename__ = "bid_info"

    bid_id: Mapped[UUID] = mapped_column(ForeignKey("bid.id", ondelete="CASCADE"), primary_key=True)
    version: Mapped[int] = mapped_column(server_default="1", primary_key=True) 

    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))

    __table_args__ = (CheckConstraint('version >= 1'),)