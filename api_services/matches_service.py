from core.api_client import APIClient


class MatchesService:
    """Service layer for match-related API operations."""

    def __init__(self, client: APIClient):
        self.client = client

    def get_matches(self):
        """Retrieve available matches."""
        return self.client.request(
            method="GET",
            endpoint="/matches",
        )