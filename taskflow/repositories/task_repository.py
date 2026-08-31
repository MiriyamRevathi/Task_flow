"""
TaskFlow Enterprise SaaS - Task Repository Data Access Layer.
Provides high-performance query methods for Task domain entities.
"""

from typing import Optional, List, Dict, Any, Set
from taskflow.models.task import Task
from taskflow.repositories.base_repository import BaseRepository
from taskflow.storage.file_storage import FileStorageEngine
from taskflow.models.enums import TaskStatus, TaskPriority


class TaskRepository(BaseRepository[Task]):
    """Data access repository for Task entities."""

    def __init__(self, storage_engine: FileStorageEngine):
        super().__init__(storage_engine, "tasks", Task)

    def get_by_project(self, project_id: str, status: Optional[str] = None) -> List[Task]:
        if not project_id:
            return []
        tasks = self.filter(lambda t: t.project_id == project_id)
        if status:
            tasks = [t for t in tasks if t.status == status]
        tasks.sort(key=lambda t: t.order_index)
        return tasks

    def get_by_workspace(self, workspace_id: str, status: Optional[str] = None) -> List[Task]:
        if not workspace_id:
            return []
        tasks = self.filter(lambda t: t.workspace_id == workspace_id)
        if status:
            tasks = [t for t in tasks if t.status == status]
        tasks.sort(key=lambda t: t.updated_at or "", reverse=True)
        return tasks

    def get_by_assignee(self, assignee_id: str, active_only: bool = True) -> List[Task]:
        if not assignee_id:
            return []
        tasks = self.filter(lambda t: t.assignee_id == assignee_id)
        if active_only:
            tasks = [t for t in tasks if t.status != TaskStatus.DONE.value]
        tasks.sort(key=lambda t: (t.priority, t.due_date or ""))
        return tasks

    def get_by_team(self, team_id: str) -> List[Task]:
        return self.filter(lambda t: t.team_id == team_id)

    def get_by_milestone(self, milestone_id: str) -> List[Task]:
        return self.filter(lambda t: t.milestone_id == milestone_id)

    def get_subtasks(self, parent_task_id: str) -> List[Task]:
        return self.filter(lambda t: t.parent_task_id == parent_task_id)

    def get_overdue_tasks(self, workspace_id: str) -> List[Task]:
        return [t for t in self.get_by_workspace(workspace_id) if t.is_overdue()]

    def get_blocked_tasks(self, workspace_id: str) -> List[Task]:
        return self.filter(lambda t: t.workspace_id == workspace_id and t.status == TaskStatus.BLOCKED.value)

    def search_tasks(self, workspace_id: str, query_str: str) -> List[Task]:
        if not query_str:
            return self.get_by_workspace(workspace_id)
        q = query_str.lower().strip()
        return self.filter(
            lambda t: t.workspace_id == workspace_id
            and (q in t.title.lower() or q in t.description.lower() or any(q in tag.lower() for tag in t.tags))
        )

    def get_task_statistics(self, workspace_id: str) -> Dict[str, Any]:
        tasks = self.get_by_workspace(workspace_id)
        total = len(tasks)

        status_counts = {s.value: 0 for s in TaskStatus}
        priority_counts = {p.value: 0 for p in TaskPriority}

        overdue_count = 0
        total_est = 0.0
        total_act = 0.0

        for t in tasks:
            if t.status in status_counts:
                status_counts[t.status] += 1
            if t.priority in priority_counts:
                priority_counts[t.priority] += 1
            if t.is_overdue():
                overdue_count += 1
            total_est += t.estimated_hours
            total_act += t.actual_hours

        done_count = status_counts.get(TaskStatus.DONE.value, 0)
        completion_rate = round((done_count / float(total)) * 100.0, 1) if total > 0 else 0.0

        return {
            "total_tasks": total,
            "status_counts": status_counts,
            "priority_counts": priority_counts,
            "overdue_count": overdue_count,
            "completion_rate": completion_rate,
            "total_estimated_hours": round(total_est, 1),
            "total_actual_hours": round(total_act, 1),
        }
