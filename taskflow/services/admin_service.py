"""
Admin Dashboard Service.
"""

from typing import Dict, Any
from taskflow.repositories.user_repository import UserRepository
from taskflow.repositories.organization_repository import OrganizationRepository
from taskflow.repositories.workspace_repository import WorkspaceRepository


class AdminService:
    def __init__(self, user_repo: UserRepository, org_repo: OrganizationRepository, workspace_repo: WorkspaceRepository):
        self.user_repo = user_repo
        self.org_repo = org_repo
        self.workspace_repo = workspace_repo

    def get_system_diagnostics(self) -> Dict[str, Any]:
        users = self.user_repo.get_all()
        orgs = self.org_repo.get_all()
        workspaces = self.workspace_repo.get_all()

        return {
            "total_users": len(users),
            "total_organizations": len(orgs),
            "total_workspaces": len(workspaces),
            "active_users": sum(1 for u in users if u.is_active),
            "super_admins": sum(1 for u in users if u.is_super_admin()),
        }
