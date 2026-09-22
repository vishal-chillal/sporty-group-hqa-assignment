


import pytest

from api_services.balance_service import BalanceService


@pytest.fixture(autouse=True)
def reset_test_state(api_client):
    """Reset the worker-scoped user before and after each test."""
    balance_service = BalanceService(api_client)

    setup_response = balance_service.reset_balance()
    setup_response.raise_for_status()

    yield

    teardown_response = balance_service.reset_balance()
    teardown_response.raise_for_status()
