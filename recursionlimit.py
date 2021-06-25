"""
Context manager for increasing the recursion limit.
"""
from contextlib import contextmanager
import sys

@contextmanager
def recursion_limit(limit):
    old_limit = sys.getrecursionlimit()

    try:
        sys.setrecursionlimit(limit)
    finally:
        sys.setrecursionlimit(old_limit)
