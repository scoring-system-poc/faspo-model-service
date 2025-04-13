import pytest
import unittest.mock
import httpx

from src.model.document import FullDocument


@pytest.fixture
def mock_score_service() -> unittest.mock.Mock:
    with unittest.mock.patch("src.api.v1.score.score") as mock_score_service:
        yield mock_score_service


@pytest.fixture
def mock_data_target_service() -> unittest.mock.Mock:
    with unittest.mock.patch("src.api.v1.score.data_target") as mock_data_target_service:
        yield mock_data_target_service


@pytest.fixture
async def async_client(mock_environ, mock_score_service, mock_data_target_service) -> httpx.AsyncClient:
    from main import app

    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_001_docs() -> list[FullDocument]:
    return [
        FullDocument(
            id=str(i),
            subject_id="1",
            type={"key": "001", "name": "doc_name", "layer": 1, "order": 1},
            period=period,
            version={"version": 1, "author": "author", "created": "1970-01-01T00:00:00"},
            sheets=[
                {
                    "id": "1",
                    "subject_id": str(i),
                    "doc_id": "1",
                    "name": "sheet_name_1",
                    "number": 1,
                    "items": [["a", "b", 1.0, 2.0, 3.0, 4.0], ["c", "d", 5.0, 6.0, 7.0, 8.0]],
                },
                {
                    "id": "2",
                    "subject_id": "1",
                    "doc_id": str(i),
                    "name": "sheet_name_2",
                    "number": 2,
                    "items": [["a", "b", 1.0, 2.0], ["c", "d", 3.0, 4.0]],
                },
            ],
        )
        for i, period in enumerate(["1970-01-01", "1971-01-01", "1972-01-01"], 1)
    ]

