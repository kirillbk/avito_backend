from httpx import Response


def check_error(response: Response, status: int):
        assert response.status_code == status
        data = response.json()
        assert "reason" in data
        assert isinstance(data["reason"], str)
        