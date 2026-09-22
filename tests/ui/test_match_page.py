import pytest

from conftest import driver
from ui_pages.match_page import MatchPage
from ui_pages.bet_slip_page import BetSlipPage

@pytest.mark.ui
def test_select_match(ui_client):
    """Verify a match can be located and an outcome can be selected."""

    ui_client.open_url(
        "https://qae-assignment-tau.vercel.app/?user-id=candidate-7MCypfTSAdl3"
    )

    match_page = MatchPage(ui_client)
    bet_slip_page = BetSlipPage(ui_client)
    
    match_id = match_page.get_upcoming_match(get_match_id_flag=True)
    home_team = match_page.get_team(match_id, "home")
    away_team = match_page.get_team(match_id, "away")

    assert home_team
    assert away_team

    match_page.select_outcome(match_id, "home")


    assert bet_slip_page.is_visible()

    assert bet_slip_page.get_selection_teams() == (
        f"{home_team} vs {away_team}"
    )

    assert "Home" in bet_slip_page.get_selection_market()

    assert bet_slip_page.get_odds()