import pytest
import unittest.mock

from src.model.document import FullDocument


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


@pytest.fixture
def mock_002_docs() -> list[FullDocument]:
    return [
        FullDocument(
            id=str(i),
            subject_id="1",
            type={"key": "002", "name": "doc_name", "layer": 1, "order": 1},
            period=period,
            version={"version": 1, "author": "author", "created": "1970-01-01T00:00:00"},
            sheets=[
                {
                    "id": "1",
                    "subject_id": "1",
                    "doc_id": str(i),
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
                    "items": [["a", "b", 1.0, 2.0, 3.0, 4.0], ["c", "d", 5.0, 6.0, 7.0, 8.0]],
                },
            ],
        )
        for i, period in enumerate(["1970-01-01", "1971-01-01", "1972-01-01"], 1)
    ]


@pytest.fixture
def mock_003_docs() -> list[FullDocument]:
    return [
        FullDocument(
            id="1",
            subject_id="1",
            type={"key": "003", "name": "doc_name", "layer": 1, "order": 1},
            period="1970-01-01",
            version={"version": 1, "author": "author", "created": "1970-01-01T00:00:00"},
            sheets=[
                {
                    "id": "1",
                    "subject_id": "1",
                    "doc_id": "1",
                    "name": "sheet_name_1",
                    "number": 1,
                    "items": [["a", 100.0], ["b", 101.0]],
                },
                {
                    "id": "2",
                    "subject_id": "1",
                    "doc_id": "1",
                    "name": "sheet_name_2",
                    "number": 2,
                    "items": [["a", 1.0, 2.0, 3.0, 4.0], ["b", 5.0, 6.0, 7.0, 8.0]],
                },
            ],
        )
    ]


@pytest.fixture
def mock_080_docs() -> list[FullDocument]:
    return [
        FullDocument(
            id="1",
            subject_id="1",
            type={"key": "080", "name": "doc_name", "layer": 1, "order": 1},
            period="1970-01-01",
            version={"version": 1, "author": "author", "created": "1970-01-01T00:00:00"},
            sheets=[
                {
                    "id": "1",
                    "subject_id": "1",
                    "doc_id": "1",
                    "name": "sheet_name_1",
                    "number": 1,
                    "items": [["a", "b", "c", "d", "e", 1.0, 2.0, 3.0, 4.0, "f", "g", "h"]],
                }
            ],
        )
    ]


@pytest.fixture
def mock_aiohttp() -> unittest.mock.AsyncMock:
    with unittest.mock.patch("aiohttp.ClientSession") as mock_aiohttp:
        mock_aiohttp.return_value = mock_aiohttp
        mock_aiohttp.post.return_value = mock_aiohttp
        mock_aiohttp.__aenter__.side_effect = mock_aiohttp

        mock_aiohttp.status = 200
        mock_aiohttp.read.side_effect = unittest.mock.AsyncMock(return_value=b"<xml>data</xml>")
        mock_aiohttp.text.side_effect = unittest.mock.AsyncMock(return_value="id")

        yield mock_aiohttp

