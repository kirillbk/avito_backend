from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from pydantic import BaseModel, Field


class ErrorResponseSchema(BaseModel):
    reason: str = Field(min_length=5)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(content=ErrorResponseSchema(reason=str(exc.detail)).model_dump(), status_code=exc.status_code)


async def system_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(content=ErrorResponseSchema(reason="Internal Server Error").model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def request_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(content=ErrorResponseSchema(reason=str(exc)).model_dump(), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)