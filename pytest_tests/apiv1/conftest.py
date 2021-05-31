import os

import pytest
from httpx import AsyncClient

from learning.app import create_app


@pytest.fixture(scope="package")
def api_test_client():
    return AsyncClient(app=create_app(os.environ["TEST_DB_URL"]), base_url="http://test")
