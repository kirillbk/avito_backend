from app.bids.schemas import (
    NewBidSchema,
    BidSchema,
    EditBidSchema,
    BidDecisionEnum,
    BidVersion,
    BidFeedback,
    BidReviewSchema,
)
from app.bids.models import BidStatusEnum
from app.error import ErrorResponse, ErrorResponseSchema
from app.database import get_db
from app.employee.crud import get_user, get_user_id
from app.organization.crud import get_user_organization_id
from app.tenders.crud import get_tender
from app.bids.crud import add_bid, get_bids_by_user

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID


router = APIRouter(prefix="/bids", tags=["bids"])


@router.post(
    "/new",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
    },
)
async def add_new_bid(
    new_bid: NewBidSchema, db: AsyncSession = Depends(get_db)
) -> BidSchema:
    user = await get_user(db, new_bid.authorId)
    if not user:
        return ErrorResponse(
            f"Пользователя {new_bid.authorId} не существует",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    organization_id = await get_user_organization_id(db, user.id)
    if not organization_id:
        return ErrorResponse(
            f"Пользователь {new_bid.authorId} не является представителем организации",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    tender = await get_tender(db, new_bid.tenderId)
    if not tender:
        return ErrorResponse(
            f"Тендера {new_bid.tenderId} не существует",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return await add_bid(db, new_bid)


@router.get(
    "/my", responses={status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema}}
)
async def get_user_bids(
    username: str, limit: int = 5, offset: int = 0, db: AsyncSession = Depends(get_db)
) -> list[BidSchema]:
    user_id = await get_user_id(db, username)
    if not user_id:
        return ErrorResponse(
            f"Пользователя {username} не существует",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return await get_bids_by_user(db, limit, offset, user_id)


@router.get("/{tender_id}/list")
async def list_tender_bids(
    tender_id: UUID, username: str, limit: int = 5, offset: int = 5
) -> list[BidSchema]:
    pass


@router.get("/{bid_id}/status")
async def get_bid_status(bid_id: UUID, username: str) -> BidStatusEnum:
    pass


@router.put("/{bid_id}/status")
async def set_bid_status(
    bid_id: UUID, status: BidStatusEnum, username: str
) -> BidSchema:
    pass


@router.patch("/{bid_id}/edit")
async def edit_bid(bid_id: UUID, username: str, bid_params: EditBidSchema) -> BidSchema:
    pass


@router.put("/{bid_id}/submit_decision")
async def bid_desiciton(
    bid_id: UUID, decision: BidDecisionEnum, username: str
) -> BidSchema:
    pass


@router.put("/{bid_id}/feedback")
async def bid_feedback(bid_id: UUID, feedback: BidFeedback, username: str) -> BidSchema:
    pass


@router.put("/{bid_id}/rollback/{version}")
async def bid_rollback(bid_id: UUID, version: BidVersion, username: str) -> BidSchema:
    pass


@router.get("/{tender_id}/reviews")
async def get_reviews(
    tender_id: UUID,
    authorUsername: str,
    requesterUsername: str,
    limit: int = 5,
    offset: int = 0,
) -> list[BidReviewSchema]:
    pass
