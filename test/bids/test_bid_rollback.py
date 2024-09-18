from test.check_error import check_error

from fastapi import status
from httpx import AsyncClient
import pytest


class TestBidVersion:
    @pytest.mark.anyio
    async def test_no_user(self, aclient: AsyncClient):
        response = await aclient.put(
            "api/bids/550e8400-e29b-41d4-a716-446655440000/rollback/1",
            params={"username": "no_user"},
        )
        check_error(response, status.HTTP_401_UNAUTHORIZED)

    @pytest.mark.anyio
    async def test_no_tender(self, aclient: AsyncClient):
        response = await aclient.put(
            "api/bids/550e8400-e29b-41d4-a716-446655440000/rollback/1",
            params={"username": "user1"},
        )
        check_error(response, status.HTTP_404_NOT_FOUND)

    @pytest.mark.anyio
    async def test_no_version(
        self, new_tender: dict[str, str], new_bid: dict[str, str], aclient: AsyncClient
    ):
        new_tender["creatorUsername"] = "user1"
        new_tender["organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        response = await aclient.post("api/tenders/new", json=new_tender)
        tender_id = response.json()["id"]

        new_bid["authorId"] = "550e8400-e29b-41d4-a716-446655440001"
        new_bid["tenderId"] = tender_id
        response = await aclient.post("api/bids/new", json=new_bid)
        bid_id = response.json()["id"]

        response = await aclient.put(
            f"api/tenders/{bid_id}/rollback/5",
            params={"username": "user1"},
        )
        check_error(response, status.HTTP_404_NOT_FOUND)

    @pytest.mark.anyio
    async def test_user_is_not_responsible(
        self, new_tender: dict[str, str], new_bid: dict[str, str], aclient: AsyncClient
    ):
        new_tender["creatorUsername"] = "user1"
        new_tender["organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        response = await aclient.post("api/tenders/new", json=new_tender)
        tender_id = response.json()["id"]

        new_bid["authorId"] = "550e8400-e29b-41d4-a716-446655440001"
        new_bid["tenderId"] = tender_id
        response = await aclient.post("api/bids/new", json=new_bid)
        bid_id = response.json()["id"]

        response = await aclient.put(
            f"api/bids/{bid_id}/rollback/1",
            params={"username": "user30"},
        )
        check_error(response, status.HTTP_403_FORBIDDEN)

    @pytest.mark.anyio
    async def test_rollback(
        self, new_tender: dict[str, str], new_bid: dict[str, str], aclient: AsyncClient
    ):
        new_tender["creatorUsername"] = "user1"
        new_tender["organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        response = await aclient.post("api/tenders/new", json=new_tender)
        tender_id = response.json()["id"]

        new_bid["authorId"] = "550e8400-e29b-41d4-a716-446655440001"
        new_bid["tenderId"] = tender_id
        response = await aclient.post("api/bids/new", json=new_bid)
        bid_id = response.json()["id"]

        new_version = {
            "name": "new_name",
            "description": "new_description",
        }
        response = await aclient.patch(
            f"api/bids/{bid_id}/edit",
            params={"username": "user1"},
            json=new_version,
        )
        response = await aclient.patch(
            f"api/bids/{bid_id}/edit",
            params={"username": "user1"},
            json=new_version,
        )

        response = await aclient.put(
            f"api/bids/{bid_id}/rollback/1",
            params={"username": "user1"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["version"] == 4
        for key, value in new_bid.items():
            assert data[key] == value

        response = await aclient.put(
            f"api/bids/{bid_id}/rollback/2",
            params={"username": "user1"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["version"] == 5
        for key, value in new_version.items():
            assert data[key] == value
