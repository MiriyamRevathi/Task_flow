"""
RBAC Service.
Provides fine-grained permission evaluation logic.
"""

from taskflow.models.user import User
from taskflow.models.enums import UserRole


class RBACService:
    @staticmethod
    def can_create_project(user: User) -> bool:
        return user.is_lead_or_above()

    @staticmethod
    def can_manage_team(user: User) -> bool:
        return user.is_manager_or_above()

    @staticmethod
    def can_access_admin_panel(user: User) -> bool:
        return user.is_org_admin()
