import pytest


@pytest.mark.asyncio
async def test_config(mock_environ) -> None:
    from src.core.config import CONFIG

    assert CONFIG.DATA_TARGET_URL == "http://faspo-store-service/api/v1/document"
    assert CONFIG.REQUIRED_DOCUMENT_TYPES == ["001", "002"]
    assert CONFIG.REQUIRED_DOCUMENT_PERIODS == 3
    assert CONFIG.OPTIONAL_CASHFLOW_DOCUMENT_TYPE == "003"
    assert CONFIG.OPTIONAL_LOAN_DOCUMENT_TYPE == "080"
    assert CONFIG.LOG_LEVEL == "INFO"

