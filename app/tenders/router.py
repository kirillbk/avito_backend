from app.tenders.schemas import (
    TenderSchema,
    NewTenderSchema,
    TenderVersion,
    EditTenderSchema,
)
from app.tenders.models import TenderServiceTypeEnum, TenderStatusEnum
from app.error import ErrorResponse, ErrorResponseSchema
from app.database import get_db
from app.employee.crud import get_user
from app.organization.crud import get_responsible
from app.tenders.crud import (
    add_tender,
    get_tenders_by_type,
    get_tenders_by_user,
    get_tender,
    update_tender,
    rollback_tender_version
)

from fastapi import APIRouter, Depends, status
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
    new_tender: NewTenderSchema, db: AsyncSession = Depends(get_db)
) -> TenderSchema:
    user = await get_user(new_tender.creatorUsername, db)
    if not user:
        return ErrorResponse(
            f"Пользователя {new_tender.creatorUsername} не существует",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    responsible = await get_responsible(user.id, new_tender.organizationId, db)
    if not responsible:
        return ErrorResponse(
            f"Пользователь {new_tender.creatorUsername} не является представителем организации {new_tender.organizationId}",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return await add_tender(
        db, user.id, **new_tender.model_dump(exclude={"creatorUsername"})
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


@router.get(
    "/{tender_id}/status",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
    },
)
async def get_tender_status(
    tender_id: UUID, username: str, db: AsyncSession = Depends(get_db)
) -> TenderStatusEnum:
    pass


@router.put("/{tender_id}/status")
async def set_tender_status(
    tender_id: UUID, status: TenderStatusEnum, username: str
) -> TenderSchema:
    pass


@router.patch(
    "/{tender_id}/edit",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
    },
)
async def edit_tender(
    tender_id: UUID,
    username: str,
    tender_info: EditTenderSchema,
    db: AsyncSession = Depends(get_db),
) -> TenderSchema:
    user = await get_user(username, db)
    if not user:
        return ErrorResponse(
            f"Пользователя {username} не существует",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    tender = await get_tender(db, tender_id)
    if not tender:
        return ErrorResponse(
            f"Тендера {tender_id} не существует", status_code=status.HTTP_404_NOT_FOUND
        )

    responsible = await get_responsible(user.id, tender.organizationId, db)
    if not responsible:
        return ErrorResponse(
            f"Пользователь {username} не является представителем организации {tender.organizationId}",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return await update_tender(db, tender_id, **tender_info.model_dump())


@router.put(
    "/{tender_id}/rollback/{version}",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
    },)
async def tender_rollback(
    tender_id: UUID, version: TenderVersion, username: str, db: AsyncSession = Depends(get_db)
) -> TenderSchema:
    user = await get_user(username, db)
    if not user:
        return ErrorResponse(
            f"Пользователя {username} не существует",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    tender = await get_tender(db, tender_id)
    if not tender:
        return ErrorResponse(
            f"Тендера {tender_id} не существует", status_code=status.HTTP_404_NOT_FOUND
        )    

    responsible = await get_responsible(user.id, tender.organizationId, db)
    if not responsible:
        return ErrorResponse(
            f"Пользователь {username} не является представителем организации {tender.organizationId}",
            status_code=status.HTTP_403_FORBIDDEN,
        )
    
    tender = await rollback_tender_version(db, tender_id, version)
    if not tender:
        return ErrorResponse(
            f"У тендера {tender_id} не существует версии {version}", status_code=status.HTTP_404_NOT_FOUND
        )           

    return tender