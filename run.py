import uvicorn

from app.config import settings


if __name__ == "__main__":
    host, port = settings.server_address.split(":")
    port = int(port)

    uvicorn.run("app.main:app", host=host, port=port)
