from httpx import AsyncClient
from fastapi import status
import pytest


class TestPing:
    @pytest.mark.anyio
    async def test_ping(self, aclient: AsyncClient):
        response = await aclient.get("api/ping")
        assert response.status_code == status.HTTP_200_OK
        assert response.text == "ok"
