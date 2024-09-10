from app.bids.schemas import NewBidSchema, BidSchema, EditBidSchema, BidDecisionEnum, BidVersion, BidFeedback, BidReviewSchema
from app.bids.models import BidStatusEnum

from fastapi import APIRouter

from uuid import UUID


router = APIRouter(prefix="/bids", tags=["bids"])


@router.post("/new")
async def add_new_bid(new_bid: NewBidSchema) -> BidSchema:
    pass


@router.get("/my")
async def get_user_bids(username: str, limit: int = 5, offset: int = 0) -> list[BidSchema]:
    pass


@router.get("/{tender_id}/list")
async def list_tender_bids(tender_id: UUID, username: str, limit: int = 5, offset: int = 5) -> list[BidSchema]:
    pass


@router.get("/{bid_id}/status")
async def get_bid_status(bid_id: UUID, username: str) -> BidStatusEnum:
    pass


@router.put("/{bid_id}/status")
async def set_bid_status(bid_id: UUID, status: BidStatusEnum, username: str) -> BidSchema:
    pass


@router.patch("/{bid_id}/edit")
async def edit_bid(bid_id: UUID, username: str, bid_params: EditBidSchema) -> BidSchema:
    pass


@router.put("/{bid_id}/submit_decision")
async def bid_desiciton(bid_id: UUID, decision: BidDecisionEnum, username: str) -> BidSchema:
    pass


@router.put("/{bid_id}/feedback")
async def bid_feedback(bid_id: UUID, feedback: BidFeedback, username: str) -> BidSchema:
    pass


@router.put("/{bid_id}/rollback/{version}")
async def bid_rollback(bid_id: UUID, version: BidVersion, username: str) -> BidSchema:
    pass


@router.get("/{tender_id}/reviews")
async def get_reviews(tender_id: UUID, authorUsername: str, requesterUsername: str, limit: int = 5, offset: int = 0) -> list[BidReviewSchema]:
    pass