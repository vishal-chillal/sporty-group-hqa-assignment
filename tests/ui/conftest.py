import logging
import os
import re
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from api_services.balance_service import BalanceService
from core.api_client import APIClient
from core.config import API_TIMEOUT, BASE_URL, TEST_USER_ID, UI_TIMEOUT
from core.ui_client import UIClient

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def api_client():
    """Create the API client used to reset UI test state."""
    return APIClient(
        base_url=BASE_URL,
        user_id=TEST_USER_ID,
        timeout=API_TIMEOUT,
    )


@pytest.fixture(autouse=True)
def reset_test_state(api_client):
    """Reset the worker-scoped user before and after each UI test."""
    balance_service = BalanceService(api_client)

    setup_response = balance_service.reset_balance()
    setup_response.raise_for_status()

    yield

    teardown_response = balance_service.reset_balance()
    teardown_response.raise_for_status()


@pytest.fixture
def ui_client(driver):
    """Create a UI client configured for the current test environment."""
    return UIClient(driver, timeout=UI_TIMEOUT)


@pytest.fixture
def driver():
    """Create and clean up a Chrome WebDriver instance for a UI test."""
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    yield driver

    driver.quit()


def pytest_runtest_makereport(item, call):
    """Capture a screenshot and browser context when a UI test fails."""
    if call.when != "call" or call.excinfo is None:
        return

    driver = item.funcargs.get("driver")
    if driver is None:
        logger.warning("UI driver unavailable; cannot capture failure screenshot")
        return

    worker_id = os.getenv("PYTEST_XDIST_WORKER", "local")
    safe_test_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", item.nodeid)
    screenshot_path = (
        Path("test-artifacts") / "screenshots" /
        f"{worker_id}-{safe_test_name}.png"
    )

    try:
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        UIClient(driver).take_screenshot(str(screenshot_path))

        screenshot = screenshot_path.read_bytes()
        allure.attach(
            screenshot,
            name=f"{worker_id}-{safe_test_name}",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            driver.current_url,
            name="Failure URL",
            attachment_type=allure.attachment_type.TEXT,
        )
        logger.info("Attached UI failure screenshot: %s", screenshot_path)
    except Exception:
        logger.exception("Unable to capture UI failure artifacts")
