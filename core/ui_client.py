import logging
import time
from typing import Optional

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


class UIClient:
    """Wrapper around Selenium WebDriver for common UI interactions."""

    def __init__(
        self,
        driver,
        timeout: int = 10,
        retry_count: int = 2,
    ):
        self.driver = driver
        self.timeout = timeout
        self.retry_count = retry_count

    def open_url(self, url: str) -> None:
        """Navigate to the specified URL."""
        logger.info("Opening URL: %s", url)
        self.driver.get(url)

    def find_element(
        self,
        by: By,
        locator: str,
        condition: str = "visible",
    ):
        """
        Locate an element and wait for the requested condition.

        Args:
            by: Selenium locator strategy.
            locator: Locator value.
            condition: Wait condition - visible, clickable, or present.

        Returns:
            WebElement.
        """

        conditions = {
            "visible": EC.visibility_of_element_located,
            "clickable": EC.element_to_be_clickable,
            "present": EC.presence_of_element_located,
        }

        if condition not in conditions:
            raise ValueError(
                f"Unsupported condition '{condition}'. "
                f"Supported conditions: {list(conditions)}"
            )

        wait_condition = conditions[condition]

        for attempt in range(self.retry_count + 1):
            try:
                logger.info(
                    "Finding element | by=%s | locator=%s | condition=%s",
                    by,
                    locator,
                    condition,
                )

                return WebDriverWait(
                    self.driver,
                    self.timeout,
                ).until(
                    wait_condition((by, locator))
                )

            except (
                StaleElementReferenceException,
                ElementNotInteractableException,
                ElementClickInterceptedException,
            ) as exc:

                if attempt == self.retry_count:
                    logger.exception(
                        "Failed to locate/interact with element after %s attempts",
                        attempt + 1,
                    )
                    raise

                logger.warning(
                    "Retrying element operation | attempt=%s/%s | error=%s",
                    attempt + 1,
                    self.retry_count + 1,
                    type(exc).__name__,
                )

                time.sleep(0.5)

        raise RuntimeError("Unexpected UI client state")

    def click(self, by: By, locator: str):
        """Wait until an element is clickable and click it."""

        element = self.find_element(
            by=by,
            locator=locator,
            condition="clickable",
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element,
        )

        element.click()

    def send_keys(self, by: By, locator: str, text: str):
        """Clear an input field and enter the supplied text."""

        element = self.find_element(
            by=by,
            locator=locator,
            condition="visible",
        )

        element.clear()
        element.send_keys(text)

    def get_text(self, by: By, locator: str) -> str:
        """Return visible text from an element."""

        element = self.find_element(
            by=by,
            locator=locator,
            condition="visible",
        )

        return element.text.strip()

    def get_attribute(
        self,
        by: By,
        locator: str,
        attribute: str,
    ) -> Optional[str]:
        """Return an element attribute value."""

        element = self.find_element(
            by=by,
            locator=locator,
            condition="present",
        )

        return element.get_attribute(attribute)

    def take_screenshot(self, file_path: str) -> None:
        """Capture the current browser screen."""

        logger.info("Taking screenshot: %s", file_path)

        self.driver.save_screenshot(file_path)


    def get_current_url(self) -> str:
        """Return the current browser URL."""
        return self.driver.current_url


    def get_title(self) -> str:
        """Return the current page title."""
        return self.driver.title

    def is_visible(
        self,
        by: By,
        locator: str,
        timeout: int = 2,
    ) -> bool:
        """Return True if an element becomes visible within the timeout."""

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, locator))
            )
            return True

        except TimeoutException:
            return False