from test.check_error import check_error

from fastapi import status
from httpx import AsyncClient
import pytest


class TestTenderList:
    @pytest.mark.anyio
    async def test_no_user(self, aclient: AsyncClient):
        response = await aclient.get(
            "api/bids/550e8400-e29b-41d4-a716-446655440000/list",
            params={"username": "no_user"},
        )
        check_error(response, status.HTTP_401_UNAUTHORIZED)

    @pytest.mark.anyio
    async def test_no_tender(self, aclient: AsyncClient):
        response = await aclient.get(
            "api/bids/550e8400-e29b-41d4-a716-446655440000/list",
            params={"username": "user1"},
        )
        check_error(response, status.HTTP_404_NOT_FOUND)

    @pytest.mark.anyio
    async def test_user_is_not_responsible(
        self, new_tender: dict[str, str], aclient: AsyncClient
    ):
        new_tender["creatorUsername"] = "user1"
        new_tender["organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        response = await aclient.post("api/tenders/new", json=new_tender)
        tender_id = response.json()["id"]

        response = await aclient.get(
            f"api/bids/{tender_id}/list", params={"username": "user30"}
        )
        check_error(response, status.HTTP_403_FORBIDDEN)

    @pytest.mark.anyio
    async def test_tender_list(
        self, new_tender: dict[str, str], new_bid: dict[str, str], aclient: AsyncClient
    ):
        new_tender["creatorUsername"] = "user1"
        new_tender["organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        response = await aclient.post("api/tenders/new", json=new_tender)
        tender_id = response.json()["id"]

        authors = (
            "550e8400-e29b-41d4-a716-446655440004",
            "550e8400-e29b-41d4-a716-446655440005",
            "550e8400-e29b-41d4-a716-446655440006",
        )
        name = "aaa", "zzz", "bbb"
        for author_id, name in zip(authors, name):
            new_bid["name"] = name
            new_bid["authorId"] = author_id
            new_bid["tenderId"] = tender_id
            await aclient.post("api/bids/new", json=new_bid)

        response = await aclient.get(
            f"api/bids/{tender_id}/list", params={"username": "user1"}
        )
        assert response.status_code == status.HTTP_200_OK
        bids = response.json()
        assert len(bids) == 3
        for bid in bids:
            assert bid["authorId"] in authors
        assert all(bids[i]["name"] <= bids[i + 1]["name"] for i in range(len(bids) - 1))
