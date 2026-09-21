import pytest

from core.api_client import APIClient
from core.config import API_TIMEOUT, BASE_URL, USER_ID
from core.logger import configure_logging


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """Configure application logging once for the test session."""
    configure_logging()


@pytest.fixture(scope="session")
def api_client():
    """Create a shared API client for the test session."""
    return APIClient(
        base_url=BASE_URL,
        user_id=USER_ID,
        timeout=API_TIMEOUT,
    )