"""
TaskFlow Enterprise SaaS - Task Domain Model.
Represents an individual work item with status workflows, assignees, subtasks, checklists, estimated/actual hours, dependencies, and comments.
Includes complete transition logic, dependency resolution helpers, checklist progress, and audit history.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List, Set
from taskflow.models.enums import TaskStatus, TaskPriority


class Task:
    """Task domain entity representing work items in Kanban board and sprint workflows."""

    VALID_STATUS_TRANSITIONS = {
        TaskStatus.BACKLOG.value: [TaskStatus.TODO.value, TaskStatus.IN_PROGRESS.value],
        TaskStatus.TODO.value: [TaskStatus.IN_PROGRESS.value, TaskStatus.BLOCKED.value, TaskStatus.BACKLOG.value],
        TaskStatus.IN_PROGRESS.value: [TaskStatus.IN_REVIEW.value, TaskStatus.BLOCKED.value, TaskStatus.TODO.value, TaskStatus.DONE.value],
        TaskStatus.IN_REVIEW.value: [TaskStatus.DONE.value, TaskStatus.IN_PROGRESS.value, TaskStatus.BLOCKED.value],
        TaskStatus.BLOCKED.value: [TaskStatus.TODO.value, TaskStatus.IN_PROGRESS.value],
        TaskStatus.DONE.value: [TaskStatus.IN_PROGRESS.value, TaskStatus.IN_REVIEW.value, TaskStatus.BACKLOG.value],
    }

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
        self.id = str(id).strip()
        self.project_id = str(project_id).strip()
        self.workspace_id = str(workspace_id).strip()
        self.title = str(title).strip()
        self.description = str(description).strip()
        self.assignee_id = assignee_id
        self.creator_id = str(creator_id).strip()
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
        self.tags = list(tags) if tags else []
        self.checklist = list(checklist) if checklist else []
        self.dependencies = list(dependencies) if dependencies else []
        self.attachments = list(attachments) if attachments else []
        self.comments = list(comments) if comments else []
        self.order_index = int(order_index)
        now_iso = datetime.now(timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso

    @property
    def status_enum(self) -> TaskStatus:
        return TaskStatus(self.status)

    @property
    def priority_enum(self) -> TaskPriority:
        return TaskPriority(self.priority)

    @property
    def is_completed(self) -> bool:
        return self.status == TaskStatus.DONE.value

    @property
    def is_blocked(self) -> bool:
        return self.status == TaskStatus.BLOCKED.value

    def is_overdue(self) -> bool:
        if not self.due_date or self.is_completed:
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

    def can_transition_to(self, target_status: str) -> bool:
        if target_status not in TaskStatus.choices():
            return False
        allowed = self.VALID_STATUS_TRANSITIONS.get(self.status, [])
        return target_status in allowed or target_status == self.status

    def set_status(self, new_status: str) -> bool:
        if new_status not in TaskStatus.choices():
            return False
        old_status = self.status
        self.status = new_status
        if new_status == TaskStatus.DONE.value and old_status != TaskStatus.DONE.value:
            self.completed_at = datetime.now(timezone.utc).isoformat()
        elif old_status == TaskStatus.DONE.value and new_status != TaskStatus.DONE.value:
            self.completed_at = None

        self.updated_at = datetime.now(timezone.utc).isoformat()
        return True

    def add_checklist_item(self, item_title: str) -> Dict[str, Any]:
        item_id = f"chk-{len(self.checklist) + 1}"
        item = {"id": item_id, "title": item_title.strip(), "completed": False, "created_at": datetime.now(timezone.utc).isoformat()}
        self.checklist.append(item)
        self.updated_at = datetime.now(timezone.utc).isoformat()
        return item

    def toggle_checklist_item(self, item_id: str) -> bool:
        for item in self.checklist:
            if item.get("id") == item_id:
                item["completed"] = not item.get("completed", False)
                self.updated_at = datetime.now(timezone.utc).isoformat()
                return True
        return False

    def add_dependency(self, parent_task_id: str):
        if parent_task_id != self.id and parent_task_id not in self.dependencies:
            self.dependencies.append(parent_task_id)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def remove_dependency(self, parent_task_id: str):
        if parent_task_id in self.dependencies:
            self.dependencies.remove(parent_task_id)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def add_comment(self, comment_id: str, author_id: str, author_name: str, content: str) -> Dict[str, Any]:
        cmt = {
            "id": comment_id,
            "author_id": author_id,
            "author_name": author_name,
            "content": content.strip(),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self.comments.append(cmt)
        self.updated_at = datetime.now(timezone.utc).isoformat()
        return cmt

    def log_hours(self, hours: float):
        self.actual_hours = round(max(0.0, self.actual_hours + float(hours)), 2)
        self.updated_at = datetime.now(timezone.utc).isoformat()

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
            "is_completed": self.is_completed,
            "is_blocked": self.is_blocked,
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

    def __repr__(self) -> str:
        return f"<Task {self.id}: {self.title} [{self.status}]>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Task):
            return False
        return self.id == other.id
