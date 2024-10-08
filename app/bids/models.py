from app.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import String, Enum, ForeignKey, CheckConstraint

from uuid import UUID
from datetime import datetime
from enum import StrEnum


class BidStatusEnum(StrEnum):
    CREATED = "Created"
    PUBLISHED = "Published"
    CANCELED = "Canceled"


class BidAuthorTypeEnum(StrEnum):
    ORGANIZATION = "Organization"
    USER = "User"


class BidVersion(Base):
    __tablename__ = "bid_version"

    id: Mapped[UUID] = mapped_column(
        server_default=func.gen_random_uuid(), primary_key=True
    )

    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))
    version: Mapped[int] = mapped_column(server_default="1")

    __table_args__ = (CheckConstraint("version >= 1"),)


class Bid(Base):
    __tablename__ = "bid"

    id: Mapped[UUID] = mapped_column(
        server_default=func.gen_random_uuid(), primary_key=True
    )

    tenderId: Mapped[UUID] = mapped_column(
        ForeignKey("tender.id", ondelete="CASCADE"), nullable=False
    )
    authorId: Mapped[UUID] = mapped_column(
        ForeignKey("employee.id", ondelete="CASCADE"), nullable=False
    )
    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE"), nullable=False
    )

    version_id: Mapped[UUID] = mapped_column(
        ForeignKey("bid_version.id", ondelete="CASCADE"), nullable=False
    )

    status: Mapped[BidStatusEnum] = mapped_column(
        Enum(BidStatusEnum), server_default=BidStatusEnum.CREATED.name, nullable=False
    )
    authorType: Mapped[BidAuthorTypeEnum] = mapped_column(
        Enum(BidAuthorTypeEnum), nullable=False
    )
    createdAt: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())

    _version: Mapped[BidVersion] = relationship()

    @property
    def name(self) -> str:
        return self._version.name

    @property
    def description(self) -> str:
        return self._version.description

    @property
    def version(self) -> int:
        return self._version.version


class BidInfo(Base):
    __tablename__ = "bid_info"

    bid_id: Mapped[UUID] = mapped_column(
        ForeignKey("bid.id", ondelete="CASCADE"), primary_key=True
    )
    bid_version_id: Mapped[UUID] = mapped_column(
        ForeignKey("bid_version.id", ondelete="CASCADE"), primary_key=True
    )


class BidReview(Base):
    __tablename__ = "bid_review"

    id: Mapped[UUID] = mapped_column(
        server_default=func.gen_random_uuid(), primary_key=True
    )

    bid_id: Mapped[UUID] = mapped_column(ForeignKey("bid.id", ondelete="CASCADE"))
    author_id: Mapped[UUID] = mapped_column(
        ForeignKey("employee.id", ondelete="CASCADE"), nullable=False
    )

    description: Mapped[str] = mapped_column(String(1000))
    createdAt: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())
