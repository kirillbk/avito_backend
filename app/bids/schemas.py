from app.bids.models import BidStatusEnum, BidAuthorTypeEnum

from pydantic import BaseModel, Field

from uuid import UUID
from datetime import datetime
from typing import Annotated, Optional
from enum import Enum


BidVersion = Annotated[int, Field(ge=1)]
BidFeedback = Annotated[str, Field(max_length=1000)]

class NewBidSchema(BaseModel):
    name: str = Field(max_length=100)
    description: str = Field(max_length=500)
    tenderId: UUID = Field(max_length=100)
    authorType: BidAuthorTypeEnum
    authorId: UUID = Field(max_length=100)


class BidSchema(NewBidSchema):
    id: UUID = Field(max_length=100)
    status: BidStatusEnum
    version: BidVersion
    createdAt: datetime


class EditBidSchema(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)


class BidReviewSchema(BaseModel):
    id: UUID = Field(max_length=100)
    description: str = Field(max_length=1000)
    createdAt: datetime


class BidDecisionEnum(str, Enum):
    APPROVED = "Approved"
    REJECTED = "Rejected"