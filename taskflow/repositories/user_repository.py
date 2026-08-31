"""
TaskFlow Enterprise SaaS - User Repository Data Access Layer.
Provides high-performance query methods for User domain entities.
"""

from typing import Optional, List, Dict, Any, Set
from taskflow.models.user import User
from taskflow.repositories.base_repository import BaseRepository
from taskflow.storage.file_storage import FileStorageEngine
from taskflow.models.enums import UserRole


class UserRepository(BaseRepository[User]):
    """Data access repository for User entities."""

    def __init__(self, storage_engine: FileStorageEngine):
        super().__init__(storage_engine, "users", User)

    def get_by_email(self, email: str) -> Optional[User]:
        if not email:
            return None
        email_clean = email.lower().strip()
        return self.find_one(lambda u: u.email == email_clean)

    def get_by_organization(self, org_id: str, active_only: bool = True) -> List[User]:
        if not org_id:
            return []
        users = self.filter(lambda u: u.organization_id == org_id)
        if active_only:
            users = [u for u in users if u.is_active]
        users.sort(key=lambda u: u.last_name)
        return users

    def get_by_workspace(self, workspace_id: str, active_only: bool = True) -> List[User]:
        if not workspace_id:
            return []
        users = self.filter(lambda u: workspace_id in u.workspace_ids or u.is_super_admin() or u.is_org_admin())
        if active_only:
            users = [u for u in users if u.is_active]
        users.sort(key=lambda u: u.first_name)
        return users

    def get_by_role(self, role: str, org_id: Optional[str] = None) -> List[User]:
        if role not in UserRole.choices():
            return []
        if org_id:
            return self.filter(lambda u: u.role == role and u.organization_id == org_id and u.is_active)
        return self.filter(lambda u: u.role == role and u.is_active)

    def get_by_department(self, department: str, org_id: str) -> List[User]:
        dept_clean = department.strip().lower()
        return self.filter(lambda u: u.organization_id == org_id and u.department.lower().strip() == dept_clean and u.is_active)

    def search_users(self, query_str: str, org_id: str) -> List[User]:
        if not query_str:
            return self.get_by_organization(org_id)
        q = query_str.lower().strip()
        return self.filter(
            lambda u: u.organization_id == org_id
            and u.is_active
            and (q in u.email or q in u.first_name.lower() or q in u.last_name.lower() or q in u.job_title.lower() or q in u.department.lower())
        )

    def get_locked_accounts(self) -> List[User]:
        return [u for u in self.get_all() if u.is_locked()]

    def count_by_organization(self, org_id: str) -> Dict[str, int]:
        users = self.get_by_organization(org_id, active_only=False)
        total = len(users)
        active = sum(1 for u in users if u.is_active)
        locked = sum(1 for u in users if u.is_locked())
        super_admins = sum(1 for u in users if u.is_super_admin())
        org_admins = sum(1 for u in users if u.role == UserRole.ORG_ADMIN.value)
        managers = sum(1 for u in users if u.role == UserRole.PROJECT_MANAGER.value)

        return {
            "total": total,
            "active": active,
            "inactive": total - active,
            "locked": locked,
            "super_admins": super_admins,
            "org_admins": org_admins,
            "managers": managers,
        }
