import pytest
import httpx


@pytest.mark.asyncio
async def test_alive(async_client: httpx.AsyncClient) -> None:
    response = await async_client.get("/alive")
    assert response.status_code == 200
    assert response.json() == "alive"


@pytest.mark.asyncio
async def test_ready(async_client: httpx.AsyncClient) -> None:
    response = await async_client.get("/ready")
    assert response.status_code == 200
    assert response.json() == "ready"

