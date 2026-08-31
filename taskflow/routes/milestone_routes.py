"""
Milestone Blueprint Routes.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from taskflow.security.rbac_middleware import login_required

milestone_bp = Blueprint("milestone", __name__, url_prefix="/milestones")


@milestone_bp.route("")
@login_required
def list_milestones():
    milestones = g.milestone_repo.get_by_workspace(g.current_workspace_id)
    return render_template("milestones/list.html", milestones=milestones)
