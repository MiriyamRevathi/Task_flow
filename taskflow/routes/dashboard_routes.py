"""
Dashboard Blueprint Routes.
"""

from flask import Blueprint, render_template, g
from taskflow.security.rbac_middleware import login_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("")
@login_required
def index():
    projects = g.project_service.get_workspace_projects(g.current_workspace_id)
    tasks = g.task_service.get_workspace_tasks(g.current_workspace_id)
    activities = g.audit_service.get_workspace_activities(g.current_workspace_id, limit=10)
    users = g.user_repo.get_by_workspace(g.current_workspace_id)

    total_projects = len(projects)
    active_projects = sum(1 for p in projects if p.status == "ACTIVE")
    open_tasks = sum(1 for t in tasks if t.status in ("TODO", "IN_PROGRESS", "IN_REVIEW"))
    overdue_tasks = sum(1 for t in tasks if t.is_overdue())

    return render_template(
        "dashboard/index.html",
        projects=projects,
        tasks=tasks,
        activities=activities,
        users=users,
        total_projects=total_projects,
        active_projects=active_projects,
        open_tasks=open_tasks,
        overdue_tasks=overdue_tasks,
    )
