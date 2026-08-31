"""
Notification Event Triggers.
"""

from typing import Dict, Any


def on_task_assigned(payload: Dict[str, Any]):
    print(f"Trigger: Task assigned notification sent for {payload.get('task_title')}")


def on_status_changed(payload: Dict[str, Any]):
    print(f"Trigger: Status changed notification sent for {payload.get('task_title')}")
