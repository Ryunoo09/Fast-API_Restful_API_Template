"""
Token Blacklist for JWT Logout.

Since JWT tokens are stateless, we use an in-memory blacklist (set) to track
tokens that have been invalidated via logout. In a production environment,
this should be replaced with a Redis store or a database table.
"""

from typing import Set

# In-memory set of blacklisted tokens
_blacklisted_tokens: Set[str] = set()


def blacklist_token(token: str) -> None:
    """Add a token to the blacklist."""
    _blacklisted_tokens.add(token)


def is_token_blacklisted(token: str) -> bool:
    """Check if a token has been blacklisted."""
    return token in _blacklisted_tokens
