"""
Workspace Repository Data Access Layer.
"""

from typing import List, Optional
from taskflow.models.workspace import Workspace
from taskflow.repositories.base_repository import BaseRepository
from taskflow.storage.file_storage import FileStorageEngine


class WorkspaceRepository(BaseRepository[Workspace]):
    def __init__(self, storage_engine: FileStorageEngine):
        super().__init__(storage_engine, "workspaces", Workspace)

    def get_by_organization(self, org_id: str) -> List[Workspace]:
        return self.filter(lambda w: w.organization_id == org_id and not w.is_archived)

    def get_user_workspaces(self, user_id: str, org_id: str, is_admin: bool = False) -> List[Workspace]:
        if is_admin:
            return self.get_by_organization(org_id)
        return self.filter(lambda w: w.organization_id == org_id and user_id in w.member_ids and not w.is_archived)
