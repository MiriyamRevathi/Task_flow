"""
ML Executive Insights Report Generator.
"""

from typing import Dict, Any


def generate_ml_insight_summary(prediction_res: Dict[str, Any]) -> str:
    return f"Project {prediction_res['project_name']} evaluated with Risk Level {prediction_res['risk_level']} (Score: {prediction_res['risk_score']})."
