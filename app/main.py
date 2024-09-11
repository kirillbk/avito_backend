from app.tenders.router import router as tenders_router
from app.bids.router import router as bids_router
from app.error import system_exception_handler, http_exception_handler, request_error_handler

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi.responses import PlainTextResponse


app = FastAPI(title="Tender Management API")
app.include_router(tenders_router, prefix="/api")
app.include_router(bids_router, prefix="/api")
app.add_exception_handler(Exception, system_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_error_handler)

@app.get("/api/ping", response_class=PlainTextResponse)
async def ping():
    return "ok"
