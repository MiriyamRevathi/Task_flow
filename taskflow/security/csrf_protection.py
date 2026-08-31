"""
CSRF Protection Utility.
"""

import os
import secrets
from flask import session, request, abort


def generate_csrf_token() -> str:
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_hex(32)
    return session["_csrf_token"]


def validate_csrf_token(token: str) -> bool:
    session_token = session.get("_csrf_token")
    if not session_token or not token:
        return False
    return secrets.compare_digest(session_token, token)
