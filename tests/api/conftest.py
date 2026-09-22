import pytest

from core.api_client import APIClient
from core.config import API_TIMEOUT, BASE_URL, TEST_USER_ID


@pytest.fixture(scope="session")
def api_client():
    """Create the shared API client for API tests in the current worker."""
    return APIClient(
        base_url=BASE_URL,
        user_id=TEST_USER_ID,
        timeout=API_TIMEOUT,
    )
