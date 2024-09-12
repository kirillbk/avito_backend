from app.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import String, Enum, ForeignKey, CheckConstraint
from sqlalchemy.ext.hybrid import hybrid_property

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


class TenderInfo(Base):
    __tablename__ = "tender_info"
    
    id: Mapped[UUID] = mapped_column(server_default=func.gen_random_uuid(), primary_key=True)
        
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))
    serviceType: Mapped[TenderServiceTypeEnum] = mapped_column(Enum(TenderServiceTypeEnum), nullable=False)


class Tender(Base):
    __tablename__ = "tender"

    id: Mapped[UUID] = mapped_column(server_default=func.gen_random_uuid(), primary_key=True)
    organizationId: Mapped[UUID] = mapped_column(ForeignKey("organization.id", ondelete="CASCADE"), nullable=False)
    creatorId: Mapped[str] = mapped_column(ForeignKey("employee.id", ondelete="CASCADE"), nullable=False)
    info_id: Mapped[UUID] = mapped_column(ForeignKey("tender_info.id", ondelete="CASCADE"), nullable=False)

    version: Mapped[int] = mapped_column(server_default="1")
    status: Mapped[TenderStatusEnum] = mapped_column(Enum(TenderStatusEnum), default=TenderStatusEnum.CREATED)
    createdAt: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())
    
    _info: Mapped["TenderInfo"] = relationship(lazy="joined") 

    @hybrid_property
    def name(self) -> str:
        return self._info.name
    
    @hybrid_property
    def description(self) -> str:
        return self._info.description
    
    @hybrid_property
    def serviceType(self) -> str:
        return self._info.serviceType
    
    __table_args__ = (
        CheckConstraint('version >= 1'),
    )


