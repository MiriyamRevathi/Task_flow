"""
Task Domain Model.
Represents an individual work item with status workflows, assignees, subtasks, checklists, estimated/actual hours, dependencies, and comments.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from taskflow.models.enums import TaskStatus, TaskPriority


class Task:
    def __init__(
        self,
        id: str,
        project_id: str,
        workspace_id: str,
        title: str,
        description: str = "",
        assignee_id: Optional[str] = None,
        creator_id: str = "",
        team_id: Optional[str] = None,
        milestone_id: Optional[str] = None,
        parent_task_id: Optional[str] = None,
        status: str = TaskStatus.TODO.value,
        priority: str = TaskPriority.MEDIUM.value,
        start_date: Optional[str] = None,
        due_date: Optional[str] = None,
        completed_at: Optional[str] = None,
        estimated_hours: float = 0.0,
        actual_hours: float = 0.0,
        tags: Optional[List[str]] = None,
        checklist: Optional[List[Dict[str, Any]]] = None,
        dependencies: Optional[List[str]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        comments: Optional[List[Dict[str, Any]]] = None,
        order_index: int = 0,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.project_id = project_id
        self.workspace_id = workspace_id
        self.title = title.strip()
        self.description = description
        self.assignee_id = assignee_id
        self.creator_id = creator_id
        self.team_id = team_id
        self.milestone_id = milestone_id
        self.parent_task_id = parent_task_id
        self.status = status if status in TaskStatus.choices() else TaskStatus.TODO.value
        self.priority = priority if priority in TaskPriority.choices() else TaskPriority.MEDIUM.value
        self.start_date = start_date
        self.due_date = due_date
        self.completed_at = completed_at
        self.estimated_hours = max(0.0, float(estimated_hours))
        self.actual_hours = max(0.0, float(actual_hours))
        self.tags = tags or []
        self.checklist = checklist or []
        self.dependencies = dependencies or []
        self.attachments = attachments or []
        self.comments = comments or []
        self.order_index = order_index
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso

    def is_overdue(self) -> bool:
        if not self.due_date or self.status == TaskStatus.DONE.value:
            return False
        try:
            due = datetime.fromisoformat(self.due_date.replace("Z", "+00:00"))
            return datetime.now(timezone.utc) > due
        except Exception:
            return False

    @property
    def checklist_progress(self) -> float:
        if not self.checklist:
            return 0.0
        done_count = sum(1 for item in self.checklist if item.get("completed", False))
        return round((done_count / len(self.checklist)) * 100.0, 1)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "workspace_id": self.workspace_id,
            "title": self.title,
            "description": self.description,
            "assignee_id": self.assignee_id,
            "creator_id": self.creator_id,
            "team_id": self.team_id,
            "milestone_id": self.milestone_id,
            "parent_task_id": self.parent_task_id,
            "status": self.status,
            "priority": self.priority,
            "start_date": self.start_date,
            "due_date": self.due_date,
            "completed_at": self.completed_at,
            "estimated_hours": self.estimated_hours,
            "actual_hours": self.actual_hours,
            "tags": self.tags,
            "checklist": self.checklist,
            "checklist_progress": self.checklist_progress,
            "dependencies": self.dependencies,
            "attachments": self.attachments,
            "comments": self.comments,
            "order_index": self.order_index,
            "is_overdue": self.is_overdue(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        return cls(
            id=data["id"],
            project_id=data["project_id"],
            workspace_id=data["workspace_id"],
            title=data["title"],
            description=data.get("description", ""),
            assignee_id=data.get("assignee_id"),
            creator_id=data.get("creator_id", ""),
            team_id=data.get("team_id"),
            milestone_id=data.get("milestone_id"),
            parent_task_id=data.get("parent_task_id"),
            status=data.get("status", TaskStatus.TODO.value),
            priority=data.get("priority", TaskPriority.MEDIUM.value),
            start_date=data.get("start_date"),
            due_date=data.get("due_date"),
            completed_at=data.get("completed_at"),
            estimated_hours=data.get("estimated_hours", 0.0),
            actual_hours=data.get("actual_hours", 0.0),
            tags=data.get("tags", []),
            checklist=data.get("checklist", []),
            dependencies=data.get("dependencies", []),
            attachments=data.get("attachments", []),
            comments=data.get("comments", []),
            order_index=data.get("order_index", 0),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
