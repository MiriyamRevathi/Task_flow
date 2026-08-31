"""
Project Blueprint Routes.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from taskflow.security.rbac_middleware import login_required

project_bp = Blueprint("project", __name__, url_prefix="/projects")


@project_bp.route("")
@login_required
def list_projects():
    projects = g.project_service.get_workspace_projects(g.current_workspace_id)
    return render_template("projects/list.html", projects=projects)


@project_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "MEDIUM")
        budget = float(request.form.get("budget", 0) or 0)
        due_date = request.form.get("due_date")

        proj, msg = g.project_service.create_project(
            workspace_id=g.current_workspace_id,
            org_id=g.current_user.organization_id or "org-100",
            name=name,
            description=description,
            owner_id=g.current_user.id,
            priority=priority,
            budget=budget,
            due_date=due_date,
        )
        if proj:
            flash(msg, "success")
            return redirect(url_for("project.detail", project_id=proj.id))
        else:
            flash(msg, "danger")

    return render_template("projects/form.html")


@project_bp.route("/<project_id>")
@login_required
def detail(project_id):
    proj = g.project_service.get_project_by_id(project_id)
    if not proj:
        flash("Project not found.", "danger")
        return redirect(url_for("project.list_projects"))

    tasks = g.task_repo.get_by_project(project_id)
    milestones = g.milestone_service.get_project_milestones(project_id)
    return render_template("projects/detail.html", project=proj, tasks=tasks, milestones=milestones)
