"""
Search Service.
Executes multi-entity search queries across projects, tasks, teams, milestones, and comments.
"""

from typing import Dict, List, Any
from taskflow.repositories.project_repository import ProjectRepository
from taskflow.repositories.task_repository import TaskRepository
from taskflow.repositories.team_repository import TeamRepository
from taskflow.repositories.milestone_repository import MilestoneRepository


class SearchService:
    def __init__(
        self,
        project_repo: ProjectRepository,
        task_repo: TaskRepository,
        team_repo: TeamRepository,
        milestone_repo: MilestoneRepository,
    ):
        self.project_repo = project_repo
        self.task_repo = task_repo
        self.team_repo = team_repo
        self.milestone_repo = milestone_repo

    def search_all(self, workspace_id: str, query: str) -> Dict[str, Any]:
        q = query.lower().strip()
        if not q:
            return {"projects": [], "tasks": [], "teams": [], "milestones": []}

        projects = [p.to_dict() for p in self.project_repo.get_by_workspace(workspace_id) if q in p.name.lower() or q in p.description.lower()]
        tasks = [t.to_dict() for t in self.task_repo.get_by_workspace(workspace_id) if q in t.title.lower() or q in t.description.lower()]
        teams = [tm.to_dict() for tm in self.team_repo.get_by_workspace(workspace_id) if q in tm.name.lower()]
        milestones = [m.to_dict() for m in self.milestone_repo.get_by_workspace(workspace_id) if q in m.title.lower()]

        return {
            "query": query,
            "projects": projects,
            "tasks": tasks,
            "teams": teams,
            "milestones": milestones,
            "total_results": len(projects) + len(tasks) + len(teams) + len(milestones),
        }
