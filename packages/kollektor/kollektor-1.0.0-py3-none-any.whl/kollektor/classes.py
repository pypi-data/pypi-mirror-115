"""
Other classes about kollektor.
"""


class Nothing:
    """None-Type replacement for Kollektor."""

    pass


class LimitExceeded(Exception):
    """Raises when limit exceeded for starting items."""

    pass
