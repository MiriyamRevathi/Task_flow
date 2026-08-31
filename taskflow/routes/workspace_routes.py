"""
Workspace Blueprint Routes.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from taskflow.security.session_manager import SessionManager
from taskflow.security.rbac_middleware import login_required

workspace_bp = Blueprint("workspace", __name__, url_prefix="/workspaces")


@workspace_bp.route("/switch/<workspace_id>")
@login_required
def switch(workspace_id):
    ws = g.workspace_repo.get_by_id(workspace_id)
    if ws and g.current_user.can_access_workspace(workspace_id):
        SessionManager.set_current_workspace_id(workspace_id)
        flash(f"Switched to workspace: {ws.name}", "success")
    else:
        flash("Unable to switch workspace.", "danger")
    return redirect(request.referrer or url_for("dashboard.index"))


@workspace_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        color = request.form.get("color_theme", "#6366f1")

        ws, msg = g.workspace_service.create_workspace(
            name=name,
            description=description,
            org_id=g.current_user.organization_id or "org-100",
            owner_id=g.current_user.id,
            color_theme=color,
        )
        if ws:
            SessionManager.set_current_workspace_id(ws.id)
            flash(msg, "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash(msg, "danger")

    return render_template("workspaces/form.html")


@workspace_bp.route("/settings")
@login_required
def settings():
    ws = g.workspace_repo.get_by_id(g.current_workspace_id)
    return render_template("workspaces/settings.html", workspace=ws)
