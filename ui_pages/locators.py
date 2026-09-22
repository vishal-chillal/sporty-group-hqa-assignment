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
