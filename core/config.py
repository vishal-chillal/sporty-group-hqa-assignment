import os
from decimal import Decimal


BASE_URL = os.getenv(
    "BASE_URL",
    "https://qae-assignment-tau.vercel.app",
)

USER_ID = os.getenv(
    "USER_ID",
    "candidate-7MCypfTSAdl3",
)

API_PREFIX = os.getenv(
    "API_PREFIX",
    "/api",
)

API_TIMEOUT = int(
    os.getenv("API_TIMEOUT", "10")
)

UI_TIMEOUT = int(os.getenv("UI_TIMEOUT", "10"))

INITIAL_BALANCE = Decimal(
    os.getenv("INITIAL_BALANCE", "125.50")
)

CURRENCY = os.getenv("CURRENCY", "EUR")

DEFAULT_STAKE = Decimal(
    os.getenv("DEFAULT_STAKE", "10.00")
)

DEFAULT_SELECTION = os.getenv("DEFAULT_SELECTION", "home")
SELECTION_LABELS = {
    "home": "Home",
    "draw": "Draw",
    "away": "Away",
}

# Test user can be overridden through TEST_USER_ID.
# Parallel execution of additional state-mutating tests may require
# isolated test users or test data.
TEST_USER_ID = os.getenv("TEST_USER_ID", USER_ID)
