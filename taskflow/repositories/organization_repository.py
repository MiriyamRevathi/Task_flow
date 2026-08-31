"""
Organization Repository Data Access Layer.
"""

from typing import Optional
from taskflow.models.organization import Organization
from taskflow.repositories.base_repository import BaseRepository
from taskflow.storage.file_storage import FileStorageEngine


class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self, storage_engine: FileStorageEngine):
        super().__init__(storage_engine, "organizations", Organization)

    def get_by_slug(self, slug: str) -> Optional[Organization]:
        slug_clean = slug.lower().strip()
        return self.find_one(lambda o: o.slug == slug_clean)
