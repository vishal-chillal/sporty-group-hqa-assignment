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

# Each xdist worker receives its own user state so API and UI tests can run safely
# in parallel. TEST_USER_ID can be set explicitly for a fixed test account.
WORKER_ID = os.getenv("PYTEST_XDIST_WORKER")
TEST_USER_ID = os.getenv(
    "TEST_USER_ID",
    f"{USER_ID}-{WORKER_ID}" if WORKER_ID else USER_ID,
)
