"""
Team Blueprint Routes.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from taskflow.security.rbac_middleware import login_required

team_bp = Blueprint("team", __name__, url_prefix="/teams")


@team_bp.route("")
@login_required
def list_teams():
    teams = g.team_service.get_workspace_teams(g.current_workspace_id)
    return render_template("teams/list.html", teams=teams)


@team_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        department = request.form.get("department", "Engineering").strip()
        description = request.form.get("description", "").strip()
        lead_id = request.form.get("lead_id", "")

        team, msg = g.team_service.create_team(
            organization_id=g.current_user.organization_id or "org-100",
            workspace_id=g.current_workspace_id,
            name=name,
            department=department,
            lead_id=lead_id,
            description=description,
        )
        if team:
            flash(msg, "success")
            return redirect(url_for("team.detail", team_id=team.id))
        else:
            flash(msg, "danger")

    users = g.user_repo.get_by_workspace(g.current_workspace_id)
    return render_template("teams/form.html", users=users)


@team_bp.route("/<team_id>")
@login_required
def detail(team_id):
    team = g.team_service.get_team_by_id(team_id)
    if not team:
        flash("Team not found.", "danger")
        return redirect(url_for("team.list_teams"))

    metrics = g.team_service.get_team_workload_metrics(team_id)
    return render_template("teams/detail.html", team=team, metrics=metrics)
