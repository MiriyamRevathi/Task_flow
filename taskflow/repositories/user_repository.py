"""
User Repository Data Access Layer.
"""

from typing import Optional, List
from taskflow.models.user import User
from taskflow.repositories.base_repository import BaseRepository
from taskflow.storage.file_storage import FileStorageEngine


class UserRepository(BaseRepository[User]):
    def __init__(self, storage_engine: FileStorageEngine):
        super().__init__(storage_engine, "users", User)

    def get_by_email(self, email: str) -> Optional[User]:
        email_clean = email.lower().strip()
        return self.find_one(lambda u: u.email == email_clean)

    def get_by_organization(self, org_id: str) -> List[User]:
        return self.filter(lambda u: u.organization_id == org_id)

    def get_by_workspace(self, workspace_id: str) -> List[User]:
        return self.filter(lambda u: workspace_id in u.workspace_ids or u.is_super_admin() or u.is_org_admin())
