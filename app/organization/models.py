
from app.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import String, Text, ForeignKey

import enum
from uuid import UUID
from datetime import date


class OrganizationTypeEnum(str, enum.Enum):
    IE = 'IE'
    LLC = 'LLC'
    JSC = 'JSC'


class Organization(Base):
    __table__ = "organization"

    id: Mapped[UUID] = mapped_column(server_default=func.gen_random_uuid(), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text())
    type: Mapped[OrganizationTypeEnum]
    created_at: Mapped[date] = mapped_column(server_default=func.current_timestamp())
    updated_at:Mapped[date] = mapped_column(server_default=func.current_timestamp())


class OrganizationResponsible(Base):
    __table__ = "organization_responsible"
    
    id: Mapped[UUID] = mapped_column(server_default=func.gen_random_uuid(), primary_key=True)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organization.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("employee", ondelete="CASCADE"), nullable=False)

