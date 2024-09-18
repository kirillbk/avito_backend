from test.check_error import check_error

from fastapi import status
from httpx import AsyncClient
import pytest


class TestMyBids:
    @pytest.mark.anyio
    async def test_no_user(self, aclient: AsyncClient):
        response = await aclient.get("api/bids/my", params={"username": "no_user"})
        check_error(response, status.HTTP_401_UNAUTHORIZED)

    @pytest.mark.anyio
    async def test_my(
        self, new_tender: dict[str, str], new_bid: dict[str, str], aclient: AsyncClient
    ):
        new_tender["creatorUsername"] = "user1"
        new_tender["organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        response = await aclient.post("api/tenders/new", json=new_tender)
        tender_id = response.json()["id"]

        new_bid["name"] = "aaa"
        new_bid["authorId"] = "550e8400-e29b-41d4-a716-446655440001"
        new_bid["tenderId"] = tender_id
        await aclient.post("api/bids/new", json=new_bid)
        new_bid["name"] = "zzz"
        new_bid["authorId"] = "550e8400-e29b-41d4-a716-446655440001"
        new_bid["tenderId"] = tender_id
        await aclient.post("api/bids/new", json=new_bid)
        new_bid["name"] = "bbb"
        new_bid["authorId"] = "550e8400-e29b-41d4-a716-446655440001"
        new_bid["tenderId"] = tender_id
        await aclient.post("api/bids/new", json=new_bid)
        new_bid["name"] = "yyy"
        new_bid["authorId"] = "550e8400-e29b-41d4-a716-44665544001e"
        new_bid["tenderId"] = tender_id
        await aclient.post("api/bids/new", json=new_bid)

        response = await aclient.get("api/bids/my", params={"username": "user1"})
        assert response.status_code == status.HTTP_200_OK
        bids = response.json()
        assert all(bids[i]["name"] <= bids[i + 1]["name"] for i in range(len(bids) - 1))
        assert len(bids) == 3
