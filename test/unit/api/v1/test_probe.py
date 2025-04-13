import pytest
import httpx


@pytest.mark.asyncio
async def test_alive(async_client: httpx.AsyncClient) -> None:
    response = await async_client.get("/api/v1/probe/alive")

    assert response.status_code == 200
    assert response.json() == {"detail": "Alive"}


@pytest.mark.asyncio
async def test_ready(async_client: httpx.AsyncClient) -> None:
    response = await async_client.get("/api/v1/probe/ready")

    assert response.status_code == 200
    assert response.json() == {"detail": "Ready"}

