from core.api_client import APIClient


class BalanceService:
    """Service layer for balance-related API operations."""

    def __init__(self, client: APIClient):
        self.client = client

    def get_balance(self):
        """Retrieve the current user balance."""
        return self.client.request(
            method="GET",
            endpoint="/balance",
        )

    def reset_balance(self):
        """Reset the user balance to the application-defined initial value."""
        return self.client.request(
            method="POST",
            endpoint="/reset-balance",
        )