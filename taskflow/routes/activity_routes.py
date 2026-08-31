"""
Activity Audit Blueprint Routes.
"""

from flask import Blueprint, render_template, g
from taskflow.security.rbac_middleware import login_required

activity_bp = Blueprint("activity", __name__, url_prefix="/activity")


@activity_bp.route("")
@login_required
def index():
    activities = g.audit_service.get_workspace_activities(g.current_workspace_id)
    return render_template("activity/index.html", activities=activities)
