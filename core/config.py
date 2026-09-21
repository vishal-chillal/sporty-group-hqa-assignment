import os


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