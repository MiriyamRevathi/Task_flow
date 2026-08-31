"""
Password Hashing & Security Module.
Provides secure password hashing using Werkzeug generate_password_hash and complexity checking.
"""

import re
from werkzeug.security import generate_password_hash, check_password_hash


class PasswordHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        return generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        if not password or not password_hash:
            return False
        return check_password_hash(password_hash, password)

    @staticmethod
    def validate_password_complexity(password: str) -> bool:
        if len(password) < 6:
            return False
        return True
