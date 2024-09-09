from app.bids.models import bidStatusEnum, authorTypeEnum

from pydantic import BaseModel, UUID4, Field

from datetime import datetime


class BidSchema(BaseModel):
    id: UUID4 = Field(max_length=100)
    name: str = Field(max_length=100)
    description: str = Field(max_length=100)
    status: bidStatusEnum
    tenderId: UUID4 = Field(max_length=100)
    authorType: authorTypeEnum
    authorId: UUID4 = Field(max_length=100)
    version: int = Field(ge=1)
    createdAt: datetime