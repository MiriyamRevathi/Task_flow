"""
Organization Service.
Manages enterprise organization settings, member limits, and multi-tenant billing simulation.
"""

from typing import Optional, Dict, Any, List, Tuple
from taskflow.repositories.organization_repository import OrganizationRepository
from taskflow.models.organization import Organization
from taskflow.utils.string_utils import slugify


class OrganizationService:
    def __init__(self, org_repo: OrganizationRepository):
        self.org_repo = org_repo

    def get_organization(self, org_id: str) -> Optional[Organization]:
        return self.org_repo.get_by_id(org_id)

    def update_settings(self, org_id: str, name: str, settings: Dict[str, Any]) -> Tuple[Optional[Organization], str]:
        org = self.org_repo.get_by_id(org_id)
        if not org:
            return None, "Organization not found."

        org.name = name
        org.slug = slugify(name)
        org.settings.update(settings)
        self.org_repo.save(org)
        return org, "Organization settings updated successfully."
