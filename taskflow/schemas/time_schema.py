"""
Time Tracking Schema Validator.
"""

from typing import Dict, Any, List


class TimeSchema:
    @staticmethod
    def validate_manual_entry(data: Dict[str, Any]) -> List[str]:
        errors = []
        if not data.get("task_id"):
            errors.append("Task selection is required.")
        if float(data.get("hours", 0) or 0) <= 0:
            errors.append("Hours logged must be greater than zero.")
        return errors
