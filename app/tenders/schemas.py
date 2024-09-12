from app.tenders.models import TenderServiceTypeEnum, TenderStatusEnum

from pydantic import BaseModel, UUID4, Field

from datetime import datetime
from uuid import UUID
from typing import Annotated, Optional


TenderVersion = Annotated[int, Field(ge=1)]


class BaseTenderSchema(BaseModel):
    name: str = Field(max_length=100)
    description: str = Field(max_length=500)
    serviceType: TenderServiceTypeEnum
    organizationId: UUID


class TenderSchema(BaseTenderSchema):
    id: UUID
    status: TenderStatusEnum
    version: TenderVersion
    createdAt: datetime


class NewTenderSchema(BaseTenderSchema):
    creatorUsername: str


class EditTenderSchema(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    serviceType: Optional[TenderServiceTypeEnum] = None
