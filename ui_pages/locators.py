class MatchLocators:
    """Locators for the match listing section."""

    MATCH_LIST_ID = "match-list"

    MATCH_CARD_ID = "match-card-{match_id}"
    MATCH_CARD_XPATH = (
        ".//div[contains(@class, 'matchCard')]"
    )
    MATCH_STATUS_XPATH = (
        ".//div[contains(@class, 'matchMeta')]"
        "//span[contains(@class, 'badge')]"
    )

    HOME_TEAM_XPATH = (
        "//div[@id='match-card-{match_id}']"
        "//div[contains(@class, 'teamRow')][1]"
        "//span[contains(@class, 'teamName')]"
    )

    AWAY_TEAM_XPATH = (
        "//div[@id='match-card-{match_id}']"
        "//div[contains(@class, 'teamRow')][2]"
        "//span[contains(@class, 'teamName')]"
    )

    ODDS_IDS = {
        "home": "odds-{match_id}-home",
        "draw": "odds-{match_id}-draw",
        "away": "odds-{match_id}-away",
    }

class BetSlipLocators:
    """Locators for the bet slip section."""

    BET_SLIP_ID = "bet-slip"

    BET_COUNT_ID = "bet-slip-count"

    SELECTION_TEAMS_CSS = ".betSelectionTeams"

    SELECTION_MARKET_CSS = ".betSelectionMarket"

    SELECTION_ODDS_CSS = ".betSelectionOdds"

    STAKE_INPUT_ID = "bet-slip-stake-input"

    TOTAL_STAKE_ID = "bet-slip-total-stake"

    POTENTIAL_PAYOUT_ID = "bet-slip-potential-payout"

    PLACE_BET_ID = "bet-slip-place-bet"

    REMOVE_ALL_ID = "bet-slip-remove-all"

    REMOVE_SELECTION_ID = "bet-slip-selection-remove"