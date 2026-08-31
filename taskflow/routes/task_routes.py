"""
Task Blueprint Routes.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from taskflow.security.rbac_middleware import login_required

task_bp = Blueprint("task", __name__, url_prefix="/tasks")


@task_bp.route("")
@login_required
def list_tasks():
    status_filter = request.args.get("status")
    tasks = g.task_service.get_workspace_tasks(g.current_workspace_id)
    if status_filter:
        tasks = [t for t in tasks if t.status == status_filter]
    return render_template("tasks/list.html", tasks=tasks, current_status=status_filter)


@task_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        project_id = request.form.get("project_id")
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        assignee_id = request.form.get("assignee_id")
        priority = request.form.get("priority", "MEDIUM")
        due_date = request.form.get("due_date")
        est_hours = float(request.form.get("estimated_hours", 0) or 0)

        task, msg = g.task_service.create_task(
            project_id=project_id,
            workspace_id=g.current_workspace_id,
            title=title,
            creator_id=g.current_user.id,
            description=description,
            assignee_id=assignee_id,
            priority=priority,
            due_date=due_date,
            estimated_hours=est_hours,
        )
        if task:
            flash(msg, "success")
            return redirect(url_for("task.detail", task_id=task.id))
        else:
            flash(msg, "danger")

    projects = g.project_repo.get_by_workspace(g.current_workspace_id)
    users = g.user_repo.get_by_workspace(g.current_workspace_id)
    return render_template("tasks/form.html", projects=projects, users=users)


@task_bp.route("/<task_id>")
@login_required
def detail(task_id):
    task = g.task_service.get_task_by_id(task_id)
    if not task:
        flash("Task not found.", "danger")
        return redirect(url_for("task.list_tasks"))

    project = g.project_repo.get_by_id(task.project_id)
    assignee = g.user_repo.get_by_id(task.assignee_id) if task.assignee_id else None
    return render_template("tasks/detail.html", task=task, project=project, assignee=assignee)


@task_bp.route("/<task_id>/status", methods=["POST"])
@login_required
def update_status(task_id):
    new_status = request.form.get("status")
    task, msg = g.task_service.update_task_status(task_id, new_status)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"success": True, "message": msg, "status": new_status})
    flash(msg, "success" if task else "danger")
    return redirect(request.referrer or url_for("task.detail", task_id=task_id))


@task_bp.route("/<task_id>/comment", methods=["POST"])
@login_required
def add_comment(task_id):
    content = request.form.get("content", "").strip()
    if content:
        g.task_service.add_comment(task_id, g.current_user.id, g.current_user.full_name, content)
        flash("Comment posted.", "success")
    return redirect(url_for("task.detail", task_id=task_id))
