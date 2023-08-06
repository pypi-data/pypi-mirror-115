"""
Find common prefix of several string, tuples of string, or other nested structure, recursively by default.
It returns the shortest prefix: empty string or empty tuple is removed.
"""

__version__ = "0.1.0"
__name__ = "k3pattern"

from .strutil import (
    common_prefix,
)


__all__ = [
    'common_prefix',
]
