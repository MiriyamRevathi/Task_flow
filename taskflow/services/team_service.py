"""
Team Management & Workload Analytics Service.
Calculates team member workload, task distribution, and department performance.
"""

from typing import List, Optional, Tuple, Dict, Any
from taskflow.repositories.team_repository import TeamRepository
from taskflow.repositories.task_repository import TaskRepository
from taskflow.repositories.user_repository import UserRepository
from taskflow.models.team import Team
from taskflow.utils.id_generator import generate_id


class TeamService:
    def __init__(self, team_repo: TeamRepository, task_repo: TaskRepository, user_repo: UserRepository):
        self.team_repo = team_repo
        self.task_repo = task_repo
        self.user_repo = user_repo

    def get_workspace_teams(self, workspace_id: str) -> List[Team]:
        return self.team_repo.get_by_workspace(workspace_id)

    def get_team_by_id(self, team_id: str) -> Optional[Team]:
        return self.team_repo.get_by_id(team_id)

    def create_team(
        self,
        organization_id: str,
        workspace_id: str,
        name: str,
        department: str = "Engineering",
        lead_id: str = "",
        description: str = "",
    ) -> Tuple[Optional[Team], str]:
        if not name:
            return None, "Team name is required."

        t_id = generate_id("team")
        team = Team(
            id=t_id,
            organization_id=organization_id,
            workspace_id=workspace_id,
            name=name,
            department=department,
            lead_id=lead_id,
            member_ids=[lead_id] if lead_id else [],
            description=description,
        )
        self.team_repo.save(team)
        return team, "Team created successfully."

    def get_team_workload_metrics(self, team_id: str) -> Dict[str, Any]:
        team = self.team_repo.get_by_id(team_id)
        if not team:
            return {}

        all_tasks = self.task_repo.get_by_workspace(team.workspace_id)
        team_members = [self.user_repo.get_by_id(uid) for uid in team.member_ids if self.user_repo.get_by_id(uid)]

        workload = []
        for member in team_members:
            m_tasks = [t for t in all_tasks if t.assignee_id == member.id]
            active_tasks = [t for t in m_tasks if t.status in ("TODO", "IN_PROGRESS", "IN_REVIEW")]
            done_tasks = [t for t in m_tasks if t.status == "DONE"]
            overdue_tasks = [t for t in m_tasks if t.is_overdue()]

            workload.append({
                "member_id": member.id,
                "member_name": member.full_name,
                "avatar_url": member.avatar_url,
                "job_title": member.job_title,
                "active_task_count": len(active_tasks),
                "done_task_count": len(done_tasks),
                "overdue_task_count": len(overdue_tasks),
                "total_estimated_hours": sum(t.estimated_hours for t in active_tasks),
            })

        return {
            "team_id": team.id,
            "team_name": team.name,
            "member_count": len(team.member_ids),
            "members_workload": workload,
        }
