"""
ML Risk Scoring Utilities.
"""

def normalize_score(raw_score: float) -> float:
    return max(0.0, min(100.0, float(raw_score)))
