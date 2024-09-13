from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from pydantic import BaseModel, Field


class ErrorResponseSchema(BaseModel):
    reason: str = Field(min_length=5)


class ErrorResponse(JSONResponse):
    def __init__(self, reason: str, status_code: int) -> None:
        super().__init__({"reason": reason}, status_code)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return ErrorResponse(str(exc.detail), exc.status_code)


async def system_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return ErrorResponse("Internal Server Error", status.HTTP_500_INTERNAL_SERVER_ERROR)


async def request_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return ErrorResponse(str(exc), status.HTTP_400_BAD_REQUEST)
