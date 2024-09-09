from app.tenders.models import tenderServiceTypeEnum, tenderStatusEnum

from pydantic import BaseModel, UUID4, Field

from datetime import datetime


class TenderSchema(BaseModel):
    id: UUID4 = Field(max_length=100)
    name: str = Field(max_length=100)
    description: str = Field(max_length=500)
    serviceType: tenderServiceTypeEnum
    status: tenderStatusEnum
    organizationId: UUID4 = Field(max_length=100)
    version: int = Field(ge=1)
    createdAt: datetime
