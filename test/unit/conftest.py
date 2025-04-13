import pytest
import unittest.mock

import os


@pytest.fixture(autouse=True)
def mock_environ(monkeypatch) -> None:
    with unittest.mock.patch.dict(os.environ, clear=True):
        env = {
            "DATA_TARGET_URL": "http://faspo-store-service/api/v1/document",
        }
        for key, value in env.items():
            monkeypatch.setenv(key, value)
        yield

