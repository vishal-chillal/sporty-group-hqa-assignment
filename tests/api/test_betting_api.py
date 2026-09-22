
from assertpy import assert_that
import allure
import pytest

from api_services.balance_service import BalanceService
from api_services.betting_service import BettingService


@allure.title("Verify that the balance returned by the reset endpoint "
"matches the balance returned by the balance endpoint.")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
class TestBettingAPI:

    @pytest.fixture(autouse=True)
    def setup_services(self, api_client):
        """Initialize services required by this test class."""
        self.balance_service = BalanceService(api_client)
        self.betting_service = BettingService(api_client)


    def test_reset_balance_consistency(self):
        """
        Verify that after resetting the balance, it is consistent and get balance returns the expected value.
        """

        reset_response = self.balance_service.reset_balance()
        # Check if the reset balance API call was successful

        assert_that(reset_response.status_code).described_as(
            "Reset balance API call failed").is_equal_to(200)
        assert_that(reset_response.json()["currency"]).described_as(
            "Reset balance API response currency is not as expected").is_equal_to("EUR")
        assert_that(reset_response.json()["message"]).described_as(
            "Reset balance API response message is not as expected").is_equal_to("Balance reset successfully")
        assert_that(reset_response.json()["balance"]).described_as(
            "Reset balance API response balance is not as expected").is_equal_to(125.5)

        reset_balance = reset_response.json()["balance"]

        # Verify that the balance after reset is consistent with the expected value
        balance_response = self.balance_service.get_balance()
        assert_that(balance_response.status_code).described_as(
            "Get balance API call failed").is_equal_to(200)
        assert_that(balance_response.json()["currency"]).described_as(
            "Get balance API response currency after balance reset is not as expected"
            ).is_equal_to("EUR")
        assert_that(balance_response.json()["balance"]).described_as(
            "Get balance API response after balance reset is not as expected"
            ).is_equal_to(reset_balance)
