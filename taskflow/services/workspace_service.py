"""
Workspace Service.
Handles workspace CRUD operations, member access control, and workspace context switching.
"""

from typing import List, Optional, Tuple, Dict, Any
from taskflow.repositories.workspace_repository import WorkspaceRepository
from taskflow.repositories.user_repository import UserRepository
from taskflow.models.workspace import Workspace
from taskflow.utils.id_generator import generate_id
from taskflow.utils.string_utils import slugify


class WorkspaceService:
    def __init__(self, workspace_repo: WorkspaceRepository, user_repo: UserRepository):
        self.workspace_repo = workspace_repo
        self.user_repo = user_repo

    def get_user_workspaces(self, user_id: str, org_id: str) -> List[Workspace]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return []
        return self.workspace_repo.get_user_workspaces(user_id, org_id, user.is_org_admin())

    def create_workspace(
        self,
        name: str,
        description: str,
        org_id: str,
        owner_id: str,
        color_theme: str = "#6366f1",
    ) -> Tuple[Optional[Workspace], str]:
        if not name:
            return None, "Workspace name is required."

        ws_id = generate_id("ws")
        slug = slugify(name)

        new_ws = Workspace(
            id=ws_id,
            organization_id=org_id,
            name=name,
            slug=slug,
            description=description,
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

        return new_ws, "Workspace created successfully."

    def add_member(self, workspace_id: str, user_id: str) -> bool:
        ws = self.workspace_repo.get_by_id(workspace_id)
        if not ws:
            return False
        ws.add_member(user_id)
        self.workspace_repo.save(ws)

        user = self.user_repo.get_by_id(user_id)
        if user and workspace_id not in user.workspace_ids:
            user.workspace_ids.append(workspace_id)
            self.user_repo.save(user)
        return True
