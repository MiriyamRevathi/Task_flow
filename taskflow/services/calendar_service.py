"""
Calendar Service.
Aggregates task deadlines, project milestones, and events into unified calendar views.
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta, timezone
from taskflow.repositories.calendar_repository import CalendarRepository
from taskflow.repositories.task_repository import TaskRepository
from taskflow.repositories.milestone_repository import MilestoneRepository
from taskflow.models.calendar_event import CalendarEvent
from taskflow.utils.id_generator import generate_id


class CalendarService:
    def __init__(
        self,
        calendar_repo: CalendarRepository,
        task_repo: TaskRepository,
        milestone_repo: MilestoneRepository,
    ):
        self.calendar_repo = calendar_repo
        self.task_repo = task_repo
        self.milestone_repo = milestone_repo

    def get_workspace_events(self, workspace_id: str) -> List[Dict[str, Any]]:
        events = []

        # 1. Custom Calendar Events
        c_events = self.calendar_repo.get_by_workspace(workspace_id)
        for e in c_events:
            events.append(e.to_dict())

        # 2. Tasks with due dates
        tasks = self.task_repo.get_by_workspace(workspace_id)
        for t in tasks:
            if t.due_date:
                events.append({
                    "id": f"evt-task-{t.id}",
                    "title": f"Task Due: {t.title}",
                    "start_time": t.due_date,
                    "event_type": "DEADLINE",
                    "link_url": f"/tasks/{t.id}",
                    "color": "#ef4444" if t.is_overdue() else "#3b82f6",
                })

        # 3. Milestones
        milestones = self.milestone_repo.get_by_workspace(workspace_id)
        for ms in milestones:
            if ms.due_date:
                events.append({
                    "id": f"evt-ms-{ms.id}",
                    "title": f"Milestone: {ms.title}",
                    "start_time": ms.due_date,
                    "event_type": "MILESTONE",
                    "link_url": f"/milestones",
                    "color": "#10b981",
                })

        return events
