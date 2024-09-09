from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI(title="Tender Management API")


@app.get("/api/ping", response_class=PlainTextResponse)
async def ping():
    return "ok"
