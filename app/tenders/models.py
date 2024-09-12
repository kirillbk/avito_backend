from app.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
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


class TenderVersion(Base):
    __tablename__ = "tender_version"
    
    id: Mapped[UUID] = mapped_column(server_default=func.gen_random_uuid(), primary_key=True)
        
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))
    serviceType: Mapped[TenderServiceTypeEnum] = mapped_column(Enum(TenderServiceTypeEnum), nullable=False)
    version: Mapped[int] = mapped_column(server_default="1")

    __table_args__ = (
        CheckConstraint('version >= 1'),
    )


class Tender(Base):
    __tablename__ = "tender"

    id: Mapped[UUID] = mapped_column(server_default=func.gen_random_uuid(), primary_key=True)
    organizationId: Mapped[UUID] = mapped_column(ForeignKey("organization.id", ondelete="CASCADE"), nullable=False)
    creatorId: Mapped[str] = mapped_column(ForeignKey("employee.id", ondelete="CASCADE"), nullable=False)
    version_id: Mapped[UUID] = mapped_column(ForeignKey("tender_version.id", ondelete="CASCADE"), nullable=False)

    status: Mapped[TenderStatusEnum] = mapped_column(Enum(TenderStatusEnum), default=TenderStatusEnum.CREATED)
    createdAt: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())
    
    _version: Mapped["TenderVersion"] = relationship() 

    @property
    def name(self) -> str:
        return self._version.name
    
    @property
    def description(self) -> str:
        return self._version.description
    
    @property
    def serviceType(self) -> str:
        return self._version.serviceType
    
    @property
    def version(self) -> int:
        return self._version.version


class TenderInfo(Base):
    __tablename__ = "tender_info"

    tender_id: Mapped[UUID] = mapped_column(ForeignKey("tender.id", ondelete="CASCADE"), primary_key=True)
    tender_version_id: Mapped[UUID] = mapped_column(ForeignKey("tender_version.id", ondelete="CASCADE"), primary_key=True)
