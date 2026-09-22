from selenium.webdriver.common.by import By

from core.ui_client import UIClient
from ui_pages.locators import HeaderLocators


class HeaderPage:
    """Page object for the header section."""

    def __init__(self, ui_client: UIClient):
        self.ui_client = ui_client
    
    def get_balance(self) -> str:
        """Return the current balance displayed in the header."""
        return self.ui_client.get_text(
            By.XPATH,
            HeaderLocators.BALANCE_XPATH,
        )

    def wait_for_balance_load(self) -> str:
        """
        Wait until the balance changes from the loading placeholder.
        """
        return self.ui_client.wait_for_text_change(
            By.XPATH,
            HeaderLocators.BALANCE_XPATH,
            "Balance: €0.00",
        )