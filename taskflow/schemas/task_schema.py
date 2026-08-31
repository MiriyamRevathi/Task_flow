"""
Task Schema Validator.
"""

from typing import Dict, Any, List


class TaskSchema:
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> List[str]:
        errors = []
        if not data.get("title"):
            errors.append("Task title is required.")
        if not data.get("project_id"):
            errors.append("Project selection is required.")
        return errors
