"""
TaskFlow Enterprise SaaS - Workspace Service.
Handles workspace creation, workspace switching, member management, invitation simulation,
and workspace archiving/restoration workflows.
"""

from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime, timezone
from taskflow.repositories.workspace_repository import WorkspaceRepository
from taskflow.repositories.user_repository import UserRepository
from taskflow.models.workspace import Workspace
from taskflow.utils.id_generator import generate_id
from taskflow.utils.string_utils import slugify


class WorkspaceService:
    """Enterprise Workspace Management Service."""

    def __init__(self, workspace_repo: WorkspaceRepository, user_repo: UserRepository):
        self.workspace_repo = workspace_repo
        self.user_repo = user_repo

    def get_user_workspaces(self, user_id: str, org_id: str) -> List[Workspace]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return []
        return self.workspace_repo.get_user_workspaces(user_id, org_id, user.is_org_admin())

    def get_workspace_by_id(self, workspace_id: str) -> Optional[Workspace]:
        return self.workspace_repo.get_by_id(workspace_id)

    def create_workspace(
        self,
        name: str,
        description: str,
        org_id: str,
        owner_id: str,
        color_theme: str = "#6366f1",
    ) -> Tuple[Optional[Workspace], str]:
        if not name or not name.strip():
            return None, "Workspace name is required."

        ws_id = generate_id("ws")
        slug = slugify(name)

        existing = self.workspace_repo.filter(lambda w: w.organization_id == org_id and w.slug == slug)
        if existing:
            return None, f"A workspace named '{name}' already exists in this organization."

        new_ws = Workspace(
            id=ws_id,
            organization_id=org_id,
            name=name.strip(),
            slug=slug,
            description=description.strip(),
            owner_id=owner_id,
            member_ids=[owner_id],
            color_theme=color_theme,
        )
        self.workspace_repo.save(new_ws)

        # Update owner's workspace list
        owner = self.user_repo.get_by_id(owner_id)
        if owner and ws_id not in owner.workspace_ids:
            owner.workspace_ids.append(ws_id)
            self.user_repo.save(owner)

        return new_ws, f"Workspace '{new_ws.name}' created successfully."

    def add_member_to_workspace(self, workspace_id: str, user_id: str) -> Tuple[bool, str]:
        ws = self.workspace_repo.get_by_id(workspace_id)
        if not ws:
            return False, "Workspace not found."

        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False, "User not found."

        if user_id in ws.member_ids:
            return False, f"User '{user.full_name}' is already a member of this workspace."

        ws.add_member(user_id)
        ws.updated_at = datetime.now(timezone.utc).isoformat()
        self.workspace_repo.save(ws)

        user.add_workspace(workspace_id)
        self.user_repo.save(user)

        return True, f"User '{user.full_name}' added to workspace successfully."

    def remove_member_from_workspace(self, workspace_id: str, user_id: str) -> Tuple[bool, str]:
        ws = self.workspace_repo.get_by_id(workspace_id)
        if not ws:
            return False, "Workspace not found."

        if user_id == ws.owner_id:
            return False, "Cannot remove the workspace owner."

        if user_id in ws.member_ids:
            ws.remove_member(user_id)
            ws.updated_at = datetime.now(timezone.utc).isoformat()
            self.workspace_repo.save(ws)

        user = self.user_repo.get_by_id(user_id)
        if user and workspace_id in user.workspace_ids:
            user.remove_workspace(workspace_id)
            self.user_repo.save(user)

        return True, "Member removed from workspace."
