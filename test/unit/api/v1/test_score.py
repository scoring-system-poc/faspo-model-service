import pytest
import httpx

from src.core.exception import HTTPException
from src.model.document import FullDocument


@pytest.mark.asyncio
async def test_score__happy_path(async_client: httpx.AsyncClient, mock_001_docs, mock_score_service) -> None:
    mock_score_service.calculate_summary_document.return_value = mock_001_docs[0]
    mock_score_service.calculate_scoring_documents.return_value = mock_001_docs
    mock_score_service.calculate_final_document.return_value = mock_001_docs[0]

    response = await async_client.post(
        "/api/v1/score",
        json=[doc.model_dump(mode="json", by_alias=True) for doc in mock_001_docs],
    )

    assert response.status_code == 201
    assert FullDocument(**response.json())


@pytest.mark.asyncio
async def test_score__http_exception(async_client: httpx.AsyncClient, mock_001_docs, mock_score_service) -> None:
    mock_score_service.calculate_final_document.side_effect = HTTPException(
        status_code=503,
        detail="Error"
    )

    response = await async_client.post(
        "/api/v1/score",
        json=[doc.model_dump(mode="json", by_alias=True) for doc in mock_001_docs],
    )

    assert response.status_code == 503
    assert response.json() == {"detail": "Error"}


@pytest.mark.asyncio
async def test_score__generic_error(async_client: httpx.AsyncClient, mock_001_docs, mock_score_service) -> None:
    mock_score_service.calculate_final_document.side_effect = ZeroDivisionError

    response = await async_client.post(
        "/api/v1/score",
        json=[doc.model_dump(mode="json", by_alias=True) for doc in mock_001_docs],
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
