from test.check_error import check_error

from fastapi import status
from httpx import AsyncClient
import pytest


class TestMy:
    @pytest.mark.anyio
    async def test_no_user(self, aclient: AsyncClient):
        response = await aclient.get("api/tenders/my", params={"username": "no_user"})
        check_error(response, status.HTTP_401_UNAUTHORIZED)

    @pytest.mark.anyio
    async def test_get(self, new_tender: dict[str, str], aclient: AsyncClient):
        new_tender["creatorUsername"] = "user1"
        new_tender[ "organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        new_tender["name"] = "aaa"
        await aclient.post("api/tenders/new", json=new_tender)
        new_tender["name"] = "zzz"
        await aclient.post("api/tenders/new", json=new_tender)
        new_tender["creatorUsername"] = "user2"
        new_tender["name"] = "bbb"
        await aclient.post("api/tenders/new", json=new_tender)
        response = await aclient.get("api/tenders/my", params={"username": "user1"})

        assert response.status_code == status.HTTP_200_OK
        tenders = response.json()
        assert len(tenders) == 2
