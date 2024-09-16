from test.check_error import check_error

from fastapi import status
from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession


class TestStatus:
    @pytest.mark.anyio
    async def test_get_no_user(self, aclient: AsyncClient):
        response = await aclient.get("api/tenders/550e8400-e29b-41d4-a716-446655440000/status", params={"username": "no_user"})
        check_error(response, status.HTTP_401_UNAUTHORIZED)
   
    @pytest.mark.anyio
    async def test_get_no_tender(self, aclient: AsyncClient):
        response = await aclient.get("api/tenders/550e8400-e29b-41d4-a716-446655440000/status", params={"username": "user1"})
        check_error(response, status.HTTP_404_NOT_FOUND)
   
    @pytest.mark.anyio
    async def test_get_user_is_not_responsible(self, new_tender: dict[str, str], aclient: AsyncClient):
        new_tender["creatorUsername"] = "user1"
        new_tender["organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        response = await aclient.post("api/tenders/new", json=new_tender)
        tender_id = response.json()["id"]

        response = await aclient.get(f"api/tenders/{tender_id}/status", params={"username": "user30"})
        check_error(response, status.HTTP_403_FORBIDDEN)

    @pytest.mark.anyio
    async def test_get(self, new_tender: dict[str, str], aclient: AsyncClient):
        new_tender["creatorUsername"] = "user1"
        new_tender["organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        response = await aclient.post("api/tenders/new", json=new_tender)
        tender_id = response.json()["id"]

        response = await aclient.get(f"api/tenders/{tender_id}/status", params={"username": "user1"})
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == "Created"

    @pytest.mark.anyio
    async def test_put_no_user(self, aclient: AsyncClient):
        response = await aclient.put("api/tenders/550e8400-e29b-41d4-a716-446655440000/status", params={"status": "Closed", "username": "no_user"})
        check_error(response, status.HTTP_401_UNAUTHORIZED)
   
    @pytest.mark.anyio
    async def test_put_no_tender(self, aclient: AsyncClient):
        response = await aclient.put("api/tenders/550e8400-e29b-41d4-a716-446655440000/status", params={"status": "Closed", "username": "user1"})
        check_error(response, status.HTTP_404_NOT_FOUND)

    @pytest.mark.anyio
    async def test_put_user_is_not_responsible(self, new_tender: dict[str, str], aclient: AsyncClient):
        new_tender["creatorUsername"] = "user1"
        new_tender["organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        response = await aclient.post("api/tenders/new", json=new_tender)
        tender_id = response.json()["id"]

        response = await aclient.put(f"api/tenders/{tender_id}/status", params={"status": "Published", "username": "user30"})
        check_error(response, status.HTTP_403_FORBIDDEN)

    @pytest.mark.anyio
    async def test_put(self, new_tender: dict[str, str], aclient: AsyncClient, db_test: AsyncSession):
        new_tender["creatorUsername"] = "user1"
        new_tender["organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        response = await aclient.post("api/tenders/new", json=new_tender)
        tender_id = response.json()["id"]

        response = await aclient.put(f"api/tenders/{tender_id}/status", params={"status": "Published", "username": "user1"})
        assert response.status_code == status.HTTP_200_OK
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "Published"