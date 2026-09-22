import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from core.api_client import APIClient
from core.ui_client import UIClient

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

@pytest.fixture
def ui_client(driver):
    """Create a UI client for interacting with the web page."""
    return UIClient(driver)

@pytest.fixture
def driver():
    """Create and clean up a Chrome WebDriver instance."""
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    yield driver

    driver.quit()