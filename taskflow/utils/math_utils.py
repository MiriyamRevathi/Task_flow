"""
Mathematical & Statistical Utilities.
"""

from typing import List


def calculate_percentage(part: float, total: float, decimals: int = 1) -> float:
    if total <= 0:
        return 0.0
    return round((part / total) * 100.0, decimals)


def average(numbers: List[float]) -> float:
    if not numbers:
        return 0.0
    return round(sum(numbers) / len(numbers), 2)


def clamp(val: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    return max(min_val, min(max_val, float(val)))
