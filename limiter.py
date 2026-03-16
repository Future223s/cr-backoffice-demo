import os
from dotenv import load_dotenv
from slowapi import Limiter
from slowapi.util import get_remote_address

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
RATE_LIMIT_DEV = os.getenv("RATE_LIMIT_DEV", "100/minute")
RATE_LIMIT_PROD = os.getenv("RATE_LIMIT_PROD", "30/minute")

DEFAULT_RATE_LIMIT = RATE_LIMIT_PROD if ENVIRONMENT == "prod" else RATE_LIMIT_DEV

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[DEFAULT_RATE_LIMIT],
)