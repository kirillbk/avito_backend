from app.tenders.router import router as tenders_router
from app.bids.router import router as bids_router

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


app = FastAPI(title="Tender Management API")
app.include_router(tenders_router, prefix="/api")
app.include_router(bids_router, prefix="/api")

@app.get("/api/ping", response_class=PlainTextResponse)
async def ping():
    return "ok"
