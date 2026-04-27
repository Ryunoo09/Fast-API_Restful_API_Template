"""
Rate Limiting Configuration (Chapter 7 Concept).

Chapter 7 uses `api.throttle` middleware with a limit of 100 requests per 5 minutes.
Here we replicate the same concept using `slowapi` for FastAPI.

Usage:
    Import `limiter` into main.py and register it as a middleware.
    Use @limiter.limit("100/5minute") decorator on any endpoint/router.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

# Create a shared limiter instance using the client's IP as the key
# Default limit: 100 requests per 5 minutes (matches Chapter 7)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/5minute"],
)
