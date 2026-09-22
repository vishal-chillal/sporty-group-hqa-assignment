from selenium.webdriver.common.by import By

from core.ui_client import UIClient
from ui_pages.locators import MatchLocators


class MatchPage:
    """Page object for the match listing section."""

    def __init__(self, ui_client: UIClient):
        self.ui_client = ui_client

    def get_upcoming_match(self, get_match_id_flag=False):
        """Return the first match card that is not marked as past."""

        match_list = self.ui_client.find_element(
            By.ID,
            MatchLocators.MATCH_LIST_ID,
            condition="visible",
        )

        cards = match_list.find_elements(
            By.XPATH,
            MatchLocators.MATCH_CARD_XPATH,
        )

        for card in cards:
            status = card.find_element(
                By.XPATH,
                MatchLocators.MATCH_STATUS_XPATH,
            ).text.strip()

            if status != "PAST":
                # If get_match_id_flag is True, return the match ID instead of the card element.
                if get_match_id_flag:
                    card_id = card.get_attribute("id")

                    prefix = "match-card-"

                    if not card_id or not card_id.startswith(prefix):
                        raise AssertionError(
                            f"Unexpected match card ID: {card_id}"
                        )

                    return card_id.removeprefix(prefix)
                return card

        raise AssertionError("No upcoming match found")

    def get_match_card(self, match_id: str):
        """Return the match card for the specified match."""

        return self.ui_client.find_element(
            By.ID,
            MatchLocators.MATCH_CARD_ID.format(match_id=match_id),
            condition="visible",
        )

    def get_team(self, match_id: str, side: str) -> str:
        """Return the home or away team name."""

        locators = {
            "home": MatchLocators.HOME_TEAM_XPATH,
            "away": MatchLocators.AWAY_TEAM_XPATH,
        }

        if side not in locators:
            raise ValueError(
                f"Invalid side '{side}'. Expected one of: home, away"
            )

        return self.ui_client.get_text(
            By.XPATH,
            locators[side].format(match_id=match_id),
        )

    def get_odds(self, match_id: str, selection: str) -> str:
        """Return odds for the specified selection."""
        if selection not in MatchLocators.ODDS_IDS:
            raise ValueError(
                f"Invalid selection '{selection}'. "
                f"Expected one of: {list(MatchLocators.ODDS_IDS)}"
            )
        return self.ui_client.get_text(
            By.ID,
            MatchLocators.ODDS_IDS[selection].format(match_id=match_id),
        )

    def select_outcome(self, match_id: str, selection: str) -> None:
        """Select the specified betting outcome."""

        if selection not in MatchLocators.ODDS_IDS:
            raise ValueError(
                f"Invalid selection '{selection}'. "
                f"Expected one of: {list(MatchLocators.ODDS_IDS)}"
            )

        self.ui_client.click(
            By.ID,
            MatchLocators.ODDS_IDS[selection].format(match_id=match_id),
        )