from selenium.webdriver.common.by import By

from core.ui_client import UIClient
from ui_pages.locators import BetSlipLocators


class BetSlipPage:
    """Page object for the bet slip section."""

    def __init__(self, ui_client: UIClient):
        self.ui_client = ui_client

    def is_visible(self) -> bool:
        """Return whether the bet slip is visible."""

        return self.ui_client.is_visible(
            By.ID,
            BetSlipLocators.BET_SLIP_ID,
        )

    def get_selection_teams(self) -> str:
        """Return the selected match teams."""

        return self.ui_client.get_text(
            By.CSS_SELECTOR,
            BetSlipLocators.SELECTION_TEAMS_CSS,
        )

    def get_selection_market(self) -> str:
        """
        Return the selected betting market and outcome.
        (who is winning, Home, Away, Draw)
        """

        return self.ui_client.get_text(
            By.CSS_SELECTOR,
            BetSlipLocators.SELECTION_MARKET_CSS,
        )

    def get_odds(self) -> str:
        """Return the selected odds."""

        return self.ui_client.get_text(
            By.CSS_SELECTOR,
            BetSlipLocators.SELECTION_ODDS_CSS,
        )

    def enter_stake(self, stake: str) -> None:
        """Enter the stake amount."""

        self.ui_client.send_keys(
            By.ID,
            BetSlipLocators.STAKE_INPUT_ID,
            stake,
        )

    def get_total_stake(self) -> str:
        """Return the displayed total stake."""

        return self.ui_client.get_text(
            By.ID,
            BetSlipLocators.TOTAL_STAKE_ID,
        )

    def get_potential_payout(self) -> str:
        """Return the displayed potential payout."""

        return self.ui_client.get_text(
            By.ID,
            BetSlipLocators.POTENTIAL_PAYOUT_ID,
        )

    def place_bet(self) -> None:
        """Place the selected bet."""

        self.ui_client.click(
            By.ID,
            BetSlipLocators.PLACE_BET_ID,
        )

    def remove_all(self) -> None:
        """Remove all selections from the bet slip."""

        self.ui_client.click(
            By.ID,
            BetSlipLocators.REMOVE_ALL_ID,
        )