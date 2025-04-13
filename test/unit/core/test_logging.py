import pytest
import unittest.mock
import logging
import datetime as dt


@pytest.mark.asyncio
async def test_setup_logging(capsys) -> None:
    with unittest.mock.patch("azure.monitor.opentelemetry"):
        from src.core.logging import setup_logging
        setup_logging()

    logging.info("Test message")
    captured = capsys.readouterr()

    assert dt.datetime.now().isoformat().replace("T", " ")[:-7] in captured.err
    assert "INFO" in captured.err
    assert "root" in captured.err
    assert "test_setup_logging" in captured.err
    assert "0000000000000000" in captured.err
    assert "Test message" in captured.err
