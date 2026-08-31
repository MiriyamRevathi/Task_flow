"""
Kanban Board Service.
Groups workspace tasks into 6 status columns and manages column card transitions.
"""

from typing import Dict, List, Any
from taskflow.repositories.task_repository import TaskRepository
from taskflow.repositories.user_repository import UserRepository
from taskflow.models.enums import TaskStatus


class KanbanService:
    COLUMNS = [
        {"id": TaskStatus.BACKLOG.value, "title": "Backlog", "color": "#64748b"},
        {"id": TaskStatus.TODO.value, "title": "To Do", "color": "#3b82f6"},
        {"id": TaskStatus.IN_PROGRESS.value, "title": "In Progress", "color": "#eab308"},
        {"id": TaskStatus.IN_REVIEW.value, "title": "In Review", "color": "#8b5cf6"},
        {"id": TaskStatus.BLOCKED.value, "title": "Blocked", "color": "#ef4444"},
        {"id": TaskStatus.DONE.value, "title": "Done", "color": "#22c55e"},
    ]

    def __init__(self, task_repo: TaskRepository, user_repo: UserRepository):
        self.task_repo = task_repo
        self.user_repo = user_repo

    def get_board_data(self, workspace_id: str, project_id: str = None) -> Dict[str, Any]:
        tasks = self.task_repo.get_by_workspace(workspace_id)
        if project_id:
            tasks = [t for t in tasks if t.project_id == project_id]

        users = {u.id: u for u in self.user_repo.get_all()}

        columns = []
        for col in self.COLUMNS:
            col_tasks = [t for t in tasks if t.status == col["id"]]
            col_tasks.sort(key=lambda t: t.order_index)

            task_cards = []
            for t in col_tasks:
                card = t.to_dict()
                assignee = users.get(t.assignee_id)
                card["assignee_name"] = assignee.full_name if assignee else "Unassigned"
                card["assignee_avatar"] = assignee.avatar_url if assignee else ""
                task_cards.append(card)

            columns.append({
                "id": col["id"],
                "title": col["title"],
                "color": col["color"],
                "count": len(task_cards),
                "tasks": task_cards
            })

        return {"columns": columns, "total_tasks": len(tasks)}
