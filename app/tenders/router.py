from app.tenders.schemas import (
    TenderSchema,
    NewTenderSchema,
    TenderVersion,
    EditTenderSchema,
)
from app.tenders.models import TenderServiceTypeEnum, TenderStatusEnum
from app.error import ErrorResponse, ErrorResponseSchema
from app.database import get_db
from app.employee.crud import get_user_id
from app.organization.crud import get_responsible_id
from app.tenders.crud import (
    add_tender,
    get_tenders_by_type,
    get_tenders_by_user,
    get_tender_status,
    get_tender_organization_id,
    update_tender_status,
    update_tender_version,
    rollback_tender_version,
)

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID
from typing import Annotated


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
    user_id = await get_user_id(db, new_tender.creatorUsername)
    if not user_id:
        return ErrorResponse(
            f"Пользователя {new_tender.creatorUsername} не существует",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    responsible_id = await get_responsible_id(db, user_id, new_tender.organizationId)
    if not responsible_id:
        return ErrorResponse(
            f"Пользователь {new_tender.creatorUsername} не является представителем организации {new_tender.organizationId}",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return await add_tender(
        db, user_id, **new_tender.model_dump(exclude={"creatorUsername"})
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
    user_id = await get_user_id(db, username)
    if not user_id:
        return ErrorResponse(
            f"Пользователя {username} не существует",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return await get_tenders_by_user(db, limit, offset, user_id)


@router.get(
    "/{tender_id}/status",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
    },
)
async def tender_status(
    tender_id: UUID, username: str | None = None, db: AsyncSession = Depends(get_db)
) -> TenderStatusEnum:
    tender_status = await get_tender_status(db, tender_id)
    if not tender_status:
        return ErrorResponse(
            f"Тендера {tender_id} не существует", status_code=status.HTTP_404_NOT_FOUND
        )

    return tender_status


@router.put(
    "/{tender_id}/status",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
    },
)
async def set_tender_status(
    tender_id: UUID,
    username: str,
    tender_status: Annotated[TenderStatusEnum, Query(alias="status")],
    db: AsyncSession = Depends(get_db),
) -> TenderSchema:
    user_id = await get_user_id(db, username)
    if not user_id:
        return ErrorResponse(
            f"Пользователя {username} не существует",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    organization_id = await get_tender_organization_id(db, tender_id)
    if not organization_id:
        return ErrorResponse(
            f"Тендера {tender_id} не существует", status_code=status.HTTP_404_NOT_FOUND
        )

    responsible_id = await get_responsible_id(db, user_id, organization_id)
    if not responsible_id:
        return ErrorResponse(
            f"Пользователь {username} не является представителем организации {organization_id}",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return await update_tender_status(db, tender_id, tender_status)


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
    user_id = await get_user_id(db, username)
    if not user_id:
        return ErrorResponse(
            f"Пользователя {username} не существует",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    tender_organization_id = await get_tender_organization_id(db, tender_id)
    if not tender_organization_id:
        return ErrorResponse(
            f"Тендера {tender_id} не существует", status_code=status.HTTP_404_NOT_FOUND
        )

    responsible_id = await get_responsible_id(db, user_id, tender_organization_id)
    if not responsible_id:
        return ErrorResponse(
            f"Пользователь {username} не является представителем организации {tender_organization_id}",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return await update_tender_version(db, tender_id, **tender_info.model_dump())


@router.put(
    "/{tender_id}/rollback/{version}",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
    },
)
async def tender_rollback(
    tender_id: UUID,
    version: TenderVersion,
    username: str,
    db: AsyncSession = Depends(get_db),
) -> TenderSchema:
    user_id = await get_user_id(db, username)
    if not user_id:
        return ErrorResponse(
            f"Пользователя {username} не существует",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    tender_organization_id = await get_tender_organization_id(db, tender_id)
    if not tender_organization_id:
        return ErrorResponse(
            f"Тендера {tender_id} не существует", status_code=status.HTTP_404_NOT_FOUND
        )

    responsible_id = await get_responsible_id(db, user_id, tender_organization_id)
    if not responsible_id:
        return ErrorResponse(
            f"Пользователь {username} не является представителем организации {tender_organization_id}",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    tender = await rollback_tender_version(db, tender_id, version)
    if not tender:
        return ErrorResponse(
            f"У тендера {tender_id} не существует версии {version}",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return tender
