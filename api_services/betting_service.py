from core.api_client import APIClient


class BettingService:
    """Service layer for betting-related API operations."""

    def __init__(self, client: APIClient):
        self.client = client

    def place_bet(self, match_id: str, selection: str, stake: float):
        """Place a single bet for a match."""
        payload = {
            "matchId": match_id,
            "selection": selection,
            "stake": stake,
        }

        return self.client.request(
            method="POST",
            endpoint="/place-bet",
            json=payload,
        )