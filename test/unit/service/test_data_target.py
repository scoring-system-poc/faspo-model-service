import pytest
import pydantic

from src.core.exception import HTTPException


class _DummyModel(pydantic.BaseModel):
    id: str


@pytest.mark.asyncio
async def test_post_data__success(mock_aiohttp) -> None:
    mock_aiohttp.status = 201

    from src.service.data_target import post_data
    from src.core.config import CONFIG

    response = await post_data(_DummyModel(id="id"), correlation_id="123")

    assert response == "id"
    mock_aiohttp.post.assert_called_once_with(
        url=f"{CONFIG.DATA_TARGET_URL}",
        headers={"Correlation-Id": "123"},
        json=_DummyModel(id="id").model_dump(mode="json", by_alias=True),
    )


@pytest.mark.asyncio
async def test_post_data__failure(mock_aiohttp) -> None:
    mock_aiohttp.status = 503
    mock_aiohttp.reason = "Service Unavailable"

    from src.service.data_target import post_data

    with pytest.raises(HTTPException) as exc_info:
        await post_data(_DummyModel(id="id"), correlation_id="123")

    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "Data target API request failed: Service Unavailable"

