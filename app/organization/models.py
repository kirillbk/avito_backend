
from app.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import String, Text, ForeignKey, Enum

import enum
from uuid import UUID
from datetime import datetime


class OrganizationTypeEnum(str, enum.Enum):
    IE = 'IE'
    LLC = 'LLC'
    JSC = 'JSC'


class Organization(Base):
    __tablename__ = "organization"

    id: Mapped[UUID] = mapped_column(server_default=func.gen_random_uuid(), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text())
    type: Mapped[OrganizationTypeEnum] = mapped_column(Enum(OrganizationTypeEnum), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())


class OrganizationResponsible(Base):
    __tablename__ = "organization_responsible"
    
    id: Mapped[UUID] = mapped_column(server_default=func.gen_random_uuid(), primary_key=True)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organization.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("employee.id", ondelete="CASCADE"), nullable=False)

