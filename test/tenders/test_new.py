from test.check_error import check_error

from httpx import AsyncClient
from fastapi import status
import pytest


class TestNew:
    @pytest.mark.anyio
    async def test_no_user(self, new_tender: dict[str, str], aclient: AsyncClient):
        new_tender["creatorUsername"] = "no_user"
        response = await aclient.post("api/tenders/new", json=new_tender)
        check_error(response, status.HTTP_401_UNAUTHORIZED)

    @pytest.mark.anyio
    async def test_user_is_not_responsible(
        self, new_tender: dict[str, str], aclient: AsyncClient
    ):
        new_tender["creatorUsername"] = "user30"
        new_tender["organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        response = await aclient.post("api/tenders/new", json=new_tender)
        check_error(response, status.HTTP_403_FORBIDDEN)

    @pytest.mark.anyio
    async def test_new_tender(self, new_tender: dict[str, str], aclient: AsyncClient):
        new_tender["creatorUsername"] = "user1"
        new_tender["organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        response = await aclient.post("api/tenders/new", json=new_tender)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        new_tender.pop("creatorUsername")
        for key, value in new_tender.items():
            value == data[key]
        assert "id" in data
        assert data["status"] == "Created"
        assert data["version"] == 1
