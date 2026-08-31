"""
Team Schema Validator.
"""

from typing import Dict, Any, List


class TeamSchema:
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> List[str]:
        errors = []
        if not data.get("name"):
            errors.append("Team name is required.")
        return errors
