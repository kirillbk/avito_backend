from app.tenders.schemas import TenderSchema, NewTenderSchema, TenderVersion, EditTenderSchema
from app.tenders.models import tenderServiceTypeEnum, tenderStatusEnum

from fastapi import APIRouter

from uuid import UUID


router = APIRouter(prefix="/tenders", tags=["tenders"])


@router.get("")
async def list_tenders(limit: int = 5, offset: int = 0, service_type: tenderServiceTypeEnum | None = None) -> list[TenderSchema]:
    pass


@router.post("/new")
async def create_new_tender(new_tender: NewTenderSchema) -> TenderSchema:
    pass


@router.get("/my")
async def get_my_tenders(username: str, limit: int = 5, offset: int = 0) -> list[TenderSchema]:
    pass


@router.get("/{tender_id}/status") 
async def get_tender_status(tender_id: UUID, username: str) -> tenderStatusEnum:
    pass


@router.put("/{tender_id}/status")
async def put_tender_status(tender_id: UUID, status: tenderStatusEnum, username: str) -> TenderSchema:
    pass


@router.patch("/{tender_id}/edit")
async def edit_tender(tender_id: UUID, username: str, tender_params: EditTenderSchema) -> TenderSchema:
    pass


@router.put("/{tender_id}/rollback/{version}")
async def rollback_tender(tender_id: UUID, version: TenderVersion, username: str) -> TenderSchema:
    pass