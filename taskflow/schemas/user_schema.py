"""
User Data Schema Validators.
"""

from typing import Dict, Any, List


class UserSchema:
    @staticmethod
    def validate_registration(data: Dict[str, Any]) -> List[str]:
        errors = []
        if not data.get("email") or "@" not in data.get("email", ""):
            errors.append("Valid email address is required.")
        if not data.get("password") or len(data.get("password", "")) < 6:
            errors.append("Password must be at least 6 characters long.")
        if not data.get("first_name"):
            errors.append("First name is required.")
        if not data.get("last_name"):
            errors.append("Last name is required.")
        return errors
