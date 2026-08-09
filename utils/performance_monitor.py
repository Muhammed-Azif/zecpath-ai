"""
utils/performance_monitor.py

Day 18: Performance monitoring utilities for Zecpath AI.

Provides lightweight execution-time measurement without changing
the behavior of existing ATS components.
"""

import logging
import time
from functools import wraps


logger = logging.getLogger(__name__)


def measure_time(operation_name: str):
    """
    Decorator that measures execution time of a function.

    The wrapped function returns exactly the same result as before.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()

            try:
                return func(*args, **kwargs)

            finally:
                elapsed = time.perf_counter() - start

                logger.info(
                    "Performance | %s | %.4f seconds",
                    operation_name,
                    elapsed,
                )

        return wrapper

    return decorator