from test.check_error import check_error

from fastapi import status
from httpx import AsyncClient
import pytest


class TestBidGetStatus:
    @pytest.mark.anyio
    async def test_no_user(self, aclient: AsyncClient):
        response = await aclient.put(
            "api/bids/550e8400-e29b-41d4-a716-446655440000/status",
            params={"username": "no_user", "status": "Published"},
        )
        check_error(response, status.HTTP_401_UNAUTHORIZED)

    @pytest.mark.anyio
    async def test_no_bid(self, aclient: AsyncClient):
        response = await aclient.put(
            "api/bids/550e8400-e29b-41d4-a716-446655440000/status",
            params={"username": "user1", "status": "Published"},
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
            f"api/bids/{bid_id}/status",
            params={"username": "user30", "status": "Published"},
        )
        check_error(response, status.HTTP_403_FORBIDDEN)

    @pytest.mark.anyio
    async def test_set_status(
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
            f"api/bids/{bid_id}/status",
            params={"username": "user1", "status": "Published"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "Published"
