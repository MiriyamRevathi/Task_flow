"""
Time Tracking Service.
Handles live work timer start/stop, manual time entry logging, billable rate calculations, and timesheets.
"""

from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime, timezone
from taskflow.repositories.time_repository import TimeRepository
from taskflow.repositories.task_repository import TaskRepository
from taskflow.models.time_entry import TimeEntry
from taskflow.utils.id_generator import generate_id


class TimeTrackingService:
    def __init__(self, time_repo: TimeRepository, task_repo: TaskRepository):
        self.time_repo = time_repo
        self.task_repo = task_repo

    def start_timer(self, user_id: str, task_id: str, description: str = "") -> Tuple[Optional[TimeEntry], str]:
        running = self.time_repo.get_running_timer(user_id)
        if running:
            return None, "You already have an active running timer. Please stop it first."

        task = self.task_repo.get_by_id(task_id)
        if not task:
            return None, "Task not found."

        entry_id = generate_id("time")
        now_iso = datetime.now(timezone.utc).isoformat()

        entry = TimeEntry(
            id=entry_id,
            user_id=user_id,
            task_id=task_id,
            project_id=task.project_id,
            workspace_id=task.workspace_id,
            description=description or f"Working on {task.title}",
            start_time=now_iso,
            is_running=True,
            hourly_rate=85.0,
        )
        self.time_repo.save(entry)
        return entry, "Timer started successfully."

    def stop_timer(self, user_id: str) -> Tuple[Optional[TimeEntry], str]:
        entry = self.time_repo.get_running_timer(user_id)
        if not entry:
            return None, "No active running timer found."

        now = datetime.now(timezone.utc)
        entry.end_time = now.isoformat()
        entry.is_running = False

        if entry.start_time:
            start_dt = datetime.fromisoformat(entry.start_time.replace("Z", "+00:00"))
            elapsed_seconds = (now - start_dt).total_seconds()
            entry.hours = round(max(0.01, elapsed_seconds / 3600.0), 2)

        self.time_repo.save(entry)

        # Update task actual hours
        task = self.task_repo.get_by_id(entry.task_id)
        if task:
            task.actual_hours = round(task.actual_hours + entry.hours, 2)
            self.task_repo.save(task)

        return entry, f"Timer stopped. Logged {entry.hours} hours."

    def get_user_timesheet(self, user_id: str) -> Dict[str, Any]:
        entries = self.time_repo.get_by_user(user_id)
        total_hours = sum(e.hours for e in entries)
        billable_hours = sum(e.hours for e in entries if e.is_billable)
        running = self.time_repo.get_running_timer(user_id)

        return {
            "entries": [e.to_dict() for e in entries],
            "total_hours": round(total_hours, 2),
            "billable_hours": round(billable_hours, 2),
            "running_timer": running.to_dict() if running else None,
        }
