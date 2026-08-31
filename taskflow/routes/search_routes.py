"""
Search Blueprint Routes.
"""

from flask import Blueprint, render_template, request, g
from taskflow.security.rbac_middleware import login_required

search_bp = Blueprint("search", __name__, url_prefix="/search")


@search_bp.route("")
@login_required
def query():
    q = request.args.get("q", "").strip()
    results = g.search_service.search_all(g.current_workspace_id, q)
    return render_template("search/results.html", results=results, query=q)
