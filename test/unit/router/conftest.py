import pytest
import unittest.mock
import fastapi
import httpx


@pytest.fixture
def app() -> fastapi.FastAPI:
    with unittest.mock.patch(
        "azure.monitor.opentelemetry.configure_azure_monitor",
        unittest.mock.MagicMock(),
    ):
        from main import app
        yield app


@pytest.fixture
async def async_client(app: fastapi.FastAPI) -> httpx.AsyncClient:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

