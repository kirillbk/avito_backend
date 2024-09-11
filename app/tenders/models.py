from app.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import String, Enum, ForeignKey, CheckConstraint

from uuid import UUID
from datetime import datetime
import enum


class TenderServiceTypeEnum(str, enum.Enum):
    CONSTRUCTION = "Construction"
    DELIVERY = "Delivery" 
    MANUFACTURE = "Manufacture"


class TenderStatusEnum(str, enum.Enum):
    CREATED = "Created"
    PUBLISHED = "Published"
    CLOSED = "Closed"


class Tender(Base):
    __tablename__ = "tender"

    id: Mapped[UUID] = mapped_column(server_default=func.gen_random_uuid(), primary_key=True)
    status: Mapped[TenderStatusEnum] = mapped_column(Enum(TenderStatusEnum), default=TenderStatusEnum.CREATED)
    organizationId: Mapped[UUID] = mapped_column(ForeignKey("organization.id", ondelete="CASCADE"), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())
    creatorUsername: Mapped[str] = mapped_column(ForeignKey("employee.username", ondelete="CASCADE"), nullable=False)


class TenderInfo(Base):
    __tablename__ = "tender_info"
    
    tender_id: Mapped[UUID] = mapped_column(ForeignKey("tender.id", ondelete="CASCADE"), primary_key=True)
    version: Mapped[int] = mapped_column(server_default="1", primary_key=True) 
    
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))
    serviceType: Mapped[TenderServiceTypeEnum] = mapped_column(Enum(TenderServiceTypeEnum), nullable=False)

    __table_args__ = (
        CheckConstraint('version >= 1'),
    )