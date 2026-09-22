from decimal import Decimal
from assertpy import assert_that
import allure
import pytest

from ui_pages.bet_slip_page import BetSlipPage
from ui_pages.header_page import HeaderPage
from ui_pages.match_page import MatchPage
from ui_pages.receipt_page import ReceiptPage


@allure.epic("Betting UI")
@allure.feature("Single Bet Placement")
@pytest.mark.ui
@pytest.mark.smoke
class TestBetPlacement:
    """End-to-end UI tests for single bet placement."""

    @pytest.fixture(autouse=True)
    def setup_pages(self, ui_client):
        """Initialize the UI client and page objects required by the test."""

        self.ui_client = ui_client
        self.match_page = MatchPage(ui_client)
        self.bet_slip_page = BetSlipPage(ui_client)
        self.receipt_page = ReceiptPage(ui_client)
        self.header_page = HeaderPage(ui_client)

    @allure.title("Verify successful single bet placement")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Verify that a user can select an upcoming match, "
        "place a valid single bet, and receive a receipt containing "
        "the correct bet details and calculated payout."
    )
    def test_successful_single_bet_placement(self):
        """Verify the complete single-bet placement flow."""

        self._open_application()

        initial_balance = self.header_page.wait_for_balance_load()
        initial_decimal_balance = Decimal(initial_balance.replace("Balance: €", ""))

        home_team, away_team = self._select_upcoming_match()

        self._verify_bet_slip(
            home_team=home_team,
            away_team=away_team,
        )

        stake, odds, expected_payout = self._enter_and_validate_stake()

        self._place_bet()

        self._verify_receipt(
            home_team=home_team,
            away_team=away_team,
            stake=stake,
            odds=odds,
            expected_payout=expected_payout,
        )
        self.receipt_page.close()
        self.ui_client.refresh_page()

        final_balance = self.header_page.wait_for_balance_load()

        final_decimal_balance = Decimal(final_balance.replace("Balance: €", ""))

        assert_that(final_decimal_balance).described_as(
            "Expected balance after bet placement"
            "should be initial balance minus stake"
            ).is_equal_to(initial_decimal_balance - stake)

    @allure.step("Open betting application")
    def _open_application(self):
        """Open the Sporty Group betting application."""

        self.ui_client.open_url(
            "https://qae-assignment-tau.vercel.app/"
            "?user-id=candidate-7MCypfTSAdl3"
        )

    @allure.step("Select first upcoming match")
    def _select_upcoming_match(self):
        """Find the first upcoming match and select the home outcome."""

        match_id = self.match_page.get_upcoming_match(
            get_match_id_flag=True
        )

        home_team = self.match_page.get_team(
            match_id,
            "home",
        )

        away_team = self.match_page.get_team(
            match_id,
            "away",
        )
        assert_that(home_team).described_as("Home team was not found").is_not_empty()
        assert_that(away_team).described_as("Away team was not found").is_not_empty()

        self.match_page.select_outcome(
            match_id,
            "home",
        )

        return home_team, away_team

    @allure.step("Verify selected match in Bet Slip")
    def _verify_bet_slip(
        self,
        home_team: str,
        away_team: str,
    ):
        """Verify the selected match and outcome appear in the Bet Slip."""

        assert_that(self.bet_slip_page.is_visible()).described_as(
            "Bet Slip is not visible after selecting an outcome"
        ).is_true()

        assert_that(self.bet_slip_page.get_selection_teams()).described_as(
            "Selected teams do not match"
        ).is_equal_to(
            f"{home_team} vs {away_team}"
        )

        assert_that(self.bet_slip_page.get_selection_market()).described_as(
            "Selected market does not match"
        ).contains("Home")

    @allure.step("Enter stake and validate potential payout")
    def _enter_and_validate_stake(self):
        """Enter a valid stake and verify the payout calculation."""

        stake = Decimal("10.00")

        self.bet_slip_page.enter_stake(
            str(stake)
        )

        actual_stake = Decimal(
            self.bet_slip_page
            .get_total_stake()
            .replace("€", "")
        )

        assert_that(actual_stake).described_as(
            f"Expected total stake €{stake:.2f}, "
            f"but found €{actual_stake:.2f}"
        ).is_equal_to(stake)

        odds_text = self.bet_slip_page.get_odds()

        odds = Decimal(
            odds_text.replace("Odds: ", "")
        )

        expected_payout = (
            stake * odds
        ).quantize(Decimal("0.01"))

        actual_payout = Decimal(
            self.bet_slip_page
            .get_potential_payout()
            .replace("€", "")
        )

        assert_that(actual_payout).described_as(
            f"Expected payout €{expected_payout:.2f}, "
            f"but found €{actual_payout:.2f}"
        ).is_equal_to(expected_payout)

        return stake, odds, expected_payout

    @allure.step("Place bet")
    def _place_bet(self):
        """Submit the selected bet."""

        self.bet_slip_page.place_bet()

    @allure.step("Verify successful bet receipt")
    def _verify_receipt(
        self,
        home_team: str,
        away_team: str,
        stake: Decimal,
        odds: Decimal,
        expected_payout: Decimal,
    ):
        """Verify all important details displayed on the bet receipt."""

        bet_id = self.receipt_page.get_bet_id()

        assert_that(bet_id).described_as(
            f"Unexpected Bet ID: {bet_id}"
        ).starts_with("#B-")


        assert_that(self.receipt_page.get_stake()).described_as(
            f"Unexpected stake: {self.receipt_page.get_stake()}"
        ).is_equal_to(
            f"€{stake:.2f}"
        )

        receipt_odds = Decimal(
            self.receipt_page.get_odds()
        )

        assert_that(receipt_odds).described_as(
            f"Unexpected odds: {receipt_odds}"
        ).is_equal_to(odds)

        receipt_payout = Decimal(
            self.receipt_page
            .get_potential_payout()
            .replace("€", "")
        )

        assert_that(receipt_payout).described_as(
            f"Unexpected payout: {receipt_payout}"
        ).is_equal_to(expected_payout)

        assert_that(self.receipt_page.get_match()).described_as(
            f"Unexpected match: {self.receipt_page.get_match()}"
        ).is_equal_to(
            f"{home_team} vs {away_team}"
        )

        assert_that(self.receipt_page.get_placed_at()).described_as(
            f"Unexpected placed at: {self.receipt_page.get_placed_at()}"
        ).is_not_none()