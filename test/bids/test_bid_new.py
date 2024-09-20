from test.check_error import check_error

from fastapi import status
from httpx import AsyncClient
import pytest


class TestBidNew:
    @pytest.mark.anyio
    async def test_no_user(self, new_bid: dict[str, str], aclient: AsyncClient):
        response = await aclient.post(
            "api/bids/new",
            json=new_bid,
        )
        check_error(response, status.HTTP_401_UNAUTHORIZED)

    @pytest.mark.anyio
    async def test_user_is_not_responsible(
        self, new_tender: dict[str, str], new_bid: dict[str, str], aclient: AsyncClient
    ):
        new_tender["creatorUsername"] = "user1"
        new_tender["organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        response = await aclient.post("api/tenders/new", json=new_tender)
        tender_id = response.json()["id"]

        new_bid["authorId"] = "550e8400-e29b-41d4-a716-44665544001e"
        new_bid["tenderId"] = tender_id
        response = await aclient.post("api/bids/new", json=new_bid)
        check_error(response, status.HTTP_403_FORBIDDEN)

    @pytest.mark.anyio
    async def test_no_tender(
        self, new_tender: dict[str, str], new_bid: dict[str, str], aclient: AsyncClient
    ):
        new_bid["authorId"] = "550e8400-e29b-41d4-a716-446655440001"
        response = await aclient.post("api/bids/new", json=new_bid)
        check_error(response, status.HTTP_404_NOT_FOUND)

    @pytest.mark.anyio
    async def test_new_tender(
        self, new_tender: dict[str, str], new_bid: dict[str, str], aclient: AsyncClient
    ):
        new_tender["creatorUsername"] = "user1"
        new_tender["organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        response = await aclient.post("api/tenders/new", json=new_tender)
        tender_id = response.json()["id"]

        new_bid["authorId"] = "550e8400-e29b-41d4-a716-446655440001"
        new_bid["tenderId"] = tender_id
        response = await aclient.post("api/bids/new", json=new_bid)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for key, val in new_bid.items():
            assert data[key] == val
        assert "id" in data
        assert "createdAt" in data
        assert data["version"] == 1
