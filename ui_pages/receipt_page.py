from selenium.webdriver.common.by import By

from core.ui_client import UIClient
from ui_pages.locators import ReceiptLocators


class ReceiptPage:
    """Page object for the successful bet receipt."""

    def __init__(self, ui_client: UIClient):
        self.ui_client = ui_client

    def get_bet_id(self) -> str:
        """Return the generated bet ID."""

        return self.ui_client.get_text(
            By.ID,
            ReceiptLocators.BET_ID,
        )

    def get_match(self) -> str:
        """Return the match displayed on the receipt."""

        return self.ui_client.get_text(
            By.ID,
            ReceiptLocators.MATCH,
        )

    def get_stake(self) -> str:
        """Return the stake displayed on the receipt."""

        return self.ui_client.get_text(
            By.ID,
            ReceiptLocators.STAKE,
        )

    def get_odds(self) -> str:
        """Return the odds displayed on the receipt."""

        return self.ui_client.get_text(
            By.ID,
            ReceiptLocators.ODDS,
        )

    def get_potential_payout(self) -> str:
        """Return the potential payout displayed on the receipt."""

        return self.ui_client.get_text(
            By.ID,
            ReceiptLocators.POTENTIAL_PAYOUT,
        )

    def get_placed_at(self) -> str:
        """Return the placement timestamp displayed on the receipt."""

        return self.ui_client.get_text(
            By.ID,
            ReceiptLocators.PLACED_AT,
        )

    def close(self) -> None:
        """Close the successful bet receipt."""

        self.ui_client.click(
            By.ID,
            ReceiptLocators.CLOSE,
        )