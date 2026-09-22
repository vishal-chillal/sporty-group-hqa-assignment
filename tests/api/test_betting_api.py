
from assertpy import assert_that
import allure
import pytest

from api_services.balance_service import BalanceService
from core.config import CURRENCY, INITIAL_BALANCE


@allure.title("Verify that the balance returned by the reset endpoint "
"matches the balance returned by the balance endpoint.")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
class TestBettingAPI:
    """API business-rule checks for the single-bet feature."""

    @pytest.fixture(autouse=True)
    def setup_services(self, api_client):
        """Initialize the balance service used by this test class."""
        self.balance_service = BalanceService(api_client)


    def test_reset_balance_consistency(self):
        """Verify reset response, persisted balance, amount, and currency agree."""

        reset_response = self.balance_service.reset_balance()
        reset_body = reset_response.json()

        assert_that(reset_response.status_code).described_as(
            "Reset balance API call failed"
        ).is_equal_to(200)
        assert_that(reset_body["currency"]).described_as(
            "Reset balance currency is incorrect"
        ).is_equal_to(CURRENCY)
        assert_that(reset_body["message"]).described_as(
            "Reset balance message is incorrect"
        ).is_equal_to("Balance reset successfully")
        assert_that(reset_body["balance"]).described_as(
            "Reset balance amount is incorrect"
        ).is_equal_to(float(INITIAL_BALANCE))

        reset_balance = reset_body["balance"]

        balance_response = self.balance_service.get_balance()
        balance_body = balance_response.json()
        assert_that(balance_response.status_code).described_as(
            "Get balance API call failed"
        ).is_equal_to(200)
        assert_that(balance_body["currency"]).described_as(
            "Persisted balance currency is incorrect"
        ).is_equal_to(CURRENCY)
        assert_that(balance_body["balance"]).described_as(
            "Persisted balance does not match reset response"
        ).is_equal_to(reset_balance)
