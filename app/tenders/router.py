from app.tenders.schemas import (
    TenderSchema,
    NewTenderSchema,
    TenderVersion,
    EditTenderSchema,
)
from app.tenders.models import TenderServiceTypeEnum, TenderStatusEnum
from app.database import get_db
from app.employee.crud import get_user
from app.organization.crud import get_responsible
from app.tenders.crud import add_tender, get_tenders_by_type, get_tenders_by_user
from app.error import ErrorResponse, ErrorResponseSchema

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID


router = APIRouter(
    prefix="/tenders",
    tags=["tenders"],
    responses={status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema}},
)


@router.get("", responses={status.HTTP_400_BAD_REQUEST: {"model": EditTenderSchema}})
async def list_tenders(
    limit: int = 5,
    offset: int = 0,
    service_type: TenderServiceTypeEnum | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[TenderSchema]:
    print(service_type)
    return await get_tenders_by_type(db, limit, offset, service_type)


@router.post(
    "/new",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponseSchema},
    },
)
async def add_new_tender(
    tender_info: NewTenderSchema, db: AsyncSession = Depends(get_db)
) -> TenderSchema:
    user = await get_user(tender_info.creatorUsername, db)
    if not user:
        return ErrorResponse(
            f"Пользователя {tender_info.creatorUsername} не существует",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    responsible = await get_responsible(user.id, tender_info.organizationId, db)
    if not responsible:
        return ErrorResponse(
            f"Пользователь {tender_info.creatorUsername} не является представителем организации {tender_info.organizationId}",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return await add_tender(
        db, user.id, **tender_info.model_dump(exclude={"creatorUsername"})
    )


@router.get(
    "/my",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
    },
)
async def get_user_tenders(
    username: str, limit: int = 5, offset: int = 0, db: AsyncSession = Depends(get_db)
) -> list[TenderSchema]:
    user = await get_user(username, db)
    if not user:
        return ErrorResponse(
            f"Пользователя {username} не существует",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return await get_tenders_by_user(db, limit, offset, user.id)


@router.get("/{tender_id}/status")
async def get_tender_status(tender_id: UUID, username: str) -> TenderStatusEnum:
    pass


@router.put("/{tender_id}/status")
async def set_tender_status(
    tender_id: UUID, status: TenderStatusEnum, username: str
) -> TenderSchema:
    pass


@router.patch("/{tender_id}/edit")
async def edit_tender(
    tender_id: UUID, username: str, tender_params: EditTenderSchema
) -> TenderSchema:
    pass


@router.put("/{tender_id}/rollback/{version}")
async def tender_rollback(
    tender_id: UUID, version: TenderVersion, username: str
) -> TenderSchema:
    pass
