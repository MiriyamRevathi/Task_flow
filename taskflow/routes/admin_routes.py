"""
Admin Blueprint Routes.
"""

from flask import Blueprint, render_template, g
from taskflow.security.rbac_middleware import roles_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("")
@roles_required("SUPER_ADMIN", "ORG_ADMIN")
def index():
    diagnostics = g.admin_service.get_system_diagnostics()
    users = g.user_repo.get_all()
    return render_template("admin/index.html", diagnostics=diagnostics, users=users)
