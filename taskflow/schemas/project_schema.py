"""
Project Schema Validator.
"""

from typing import Dict, Any, List


class ProjectSchema:
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> List[str]:
        errors = []
        if not data.get("name"):
            errors.append("Project name is required.")
        return errors
