"""
Milestone Service.
"""

from typing import List, Optional, Tuple
from taskflow.repositories.milestone_repository import MilestoneRepository
from taskflow.models.milestone import Milestone
from taskflow.utils.id_generator import generate_id


class MilestoneService:
    def __init__(self, milestone_repo: MilestoneRepository):
        self.milestone_repo = milestone_repo

    def get_project_milestones(self, project_id: str) -> List[Milestone]:
        return self.milestone_repo.get_by_project(project_id)

    def create_milestone(
        self,
        project_id: str,
        workspace_id: str,
        title: str,
        description: str = "",
        due_date: Optional[str] = None,
    ) -> Tuple[Optional[Milestone], str]:
        if not title:
            return None, "Milestone title is required."

        ms_id = generate_id("ms")
        ms = Milestone(
            id=ms_id,
            project_id=project_id,
            workspace_id=workspace_id,
            title=title,
            description=description,
            due_date=due_date,
        )
        self.milestone_repo.save(ms)
        return ms, "Milestone created successfully."
