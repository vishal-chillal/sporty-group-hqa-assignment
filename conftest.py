import pytest

from core.logger import configure_logging


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """Configure application logging once for the test session."""
    configure_logging()
