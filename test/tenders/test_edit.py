from test.check_error import check_error

from fastapi import status
from httpx import AsyncClient
import pytest


class TestEdit:
    @pytest.mark.anyio
    async def test_no_user(self, aclient: AsyncClient):
        response = await aclient.patch(
            "api/tenders/550e8400-e29b-41d4-a716-446655440000/edit",
            params={"username": "no_user"},
            json={
                "name": "string",
                "description": "string",
                "serviceType": "Construction",
            },
        )
        check_error(response, status.HTTP_401_UNAUTHORIZED)

    @pytest.mark.anyio
    async def test_no_tender(self, aclient: AsyncClient):
        response = await aclient.patch(
            "api/tenders/550e8400-e29b-41d4-a716-446655440000/edit",
            params={"username": "user1"},
            json={
                "name": "string",
                "description": "string",
                "serviceType": "Construction",
            },
        )
        check_error(response, status.HTTP_404_NOT_FOUND)

    @pytest.mark.anyio
    async def test_user_is_not_responsible(self, new_tender, aclient: AsyncClient):
        new_tender["creatorUsername"] = "user1"
        new_tender["organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        response = await aclient.post("api/tenders/new", json=new_tender)
        tender_id = response.json()["id"]

        response = await aclient.patch(
            f"api/tenders/{tender_id}/edit",
            params={"username": "user30"},
            json={
                "name": "string",
                "description": "string",
                "serviceType": "Construction",
            },
        )
        check_error(response, status.HTTP_403_FORBIDDEN)

    @pytest.mark.anyio
    async def test_edit(self, new_tender: dict[str, str], aclient: AsyncClient):
        new_tender["creatorUsername"] = "user1"
        new_tender["organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        response = await aclient.post("api/tenders/new", json=new_tender)
        tender_id = response.json()["id"]

        new_version = {
            "name": "new_name",
            "description": "new_description",
        }
        response = await aclient.patch(
            f"api/tenders/{tender_id}/edit",
            params={"username": "user1"},
            json=new_version,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["version"] == 2
        for key, value in new_version.items():
            data[key] == value
        assert data["serviceType"] == new_tender["serviceType"]
