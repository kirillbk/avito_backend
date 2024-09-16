from httpx import AsyncClient
from fastapi import status
import pytest


class TestTenders:
    @pytest.mark.anyio
    async def test_tenders(self, new_tender: dict[str, str], aclient: AsyncClient):
        new_tender["creatorUsername"] = "user1"
        new_tender[ "organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        new_tender["name"] = "aaa"
        await aclient.post("api/tenders/new", json=new_tender)
        new_tender["name"] = "zzz"
        await aclient.post("api/tenders/new", json=new_tender)
        new_tender["name"] = "bbb"
        await aclient.post("api/tenders/new", json=new_tender)
        response = await aclient.get("api/tenders")
        
        assert response.status_code == status.HTTP_200_OK
        tenders = response.json()
        assert len(tenders) == 3
        assert all(tenders[i]["name"] <= tenders[i + 1]["name"] for i in range(len(tenders) - 1))
        new_tender.pop("creatorUsername")
        for key, value in new_tender.items():
            value == tenders[-1][key]
        assert "id" in tenders[-1]
        assert tenders[-1]["status"] == "Created"
        assert tenders[-1]["version"] == 1

    @pytest.mark.anyio
    async def test_tenders_type(self, new_tender: dict[str, str], aclient: AsyncClient):
        new_tender["creatorUsername"] = "user1"
        new_tender[ "organizationId"] = "550e8400-e29b-41d4-a716-446655440020"
        new_tender["name"] = "aaa"
        await aclient.post("api/tenders/new", json=new_tender)
        new_tender["name"] = "zzz"
        await aclient.post("api/tenders/new", json=new_tender)
        new_tender["name"] = "bbb"
        new_tender["serviceType"] = "Delivery"
        response = await aclient.post("api/tenders/new", json=new_tender)
        
        assert response.status_code == status.HTTP_200_OK
        response = await aclient.get("api/tenders", params={"service_type": "Construction"})
        tenders = response.json()
        assert len(tenders) == 2

        response = await aclient.get("api/tenders", params={"service_type": "Delivery"})
        tenders = response.json()
        assert len(tenders) == 1
