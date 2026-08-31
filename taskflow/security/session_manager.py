"""
Session Manager.
Manages secure user sessions stored in Flask session cookies and memory.
"""

from flask import session
from typing import Optional, Dict, Any


class SessionManager:
    SESSION_KEY_USER_ID = "user_id"
    SESSION_KEY_ORG_ID = "org_id"
    SESSION_KEY_WORKSPACE_ID = "workspace_id"
    SESSION_KEY_ROLE = "user_role"

    @classmethod
    def login_user(cls, user_id: str, org_id: str, default_workspace_id: str, role: str):
        session.clear()
        session[cls.SESSION_KEY_USER_ID] = user_id
        session[cls.SESSION_KEY_ORG_ID] = org_id
        session[cls.SESSION_KEY_WORKSPACE_ID] = default_workspace_id
        session[cls.SESSION_KEY_ROLE] = role
        session.permanent = True

    @classmethod
    def logout_user(cls):
        session.clear()

    @classmethod
    def get_current_user_id(cls) -> Optional[str]:
        return session.get(cls.SESSION_KEY_USER_ID)

    @classmethod
    def get_current_workspace_id(cls) -> Optional[str]:
        return session.get(cls.SESSION_KEY_WORKSPACE_ID)

    @classmethod
    def set_current_workspace_id(cls, workspace_id: str):
        session[cls.SESSION_KEY_WORKSPACE_ID] = workspace_id

    @classmethod
    def get_current_role(cls) -> Optional[str]:
        return session.get(cls.SESSION_KEY_ROLE)

    @classmethod
    def is_authenticated(cls) -> bool:
        return cls.SESSION_KEY_USER_ID in session
