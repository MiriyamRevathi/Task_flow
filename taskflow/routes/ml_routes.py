"""
ML Risk Insights Blueprint Routes.
"""

from flask import Blueprint, render_template, jsonify, g
from taskflow.security.rbac_middleware import login_required

ml_bp = Blueprint("ml", __name__, url_prefix="/ml-insights")


@ml_bp.route("")
@login_required
def index():
    projects = g.project_service.get_workspace_projects(g.current_workspace_id)
    insights = []
    for p in projects:
        res = g.ml_service.get_project_risk_insights(p.id)
        if res:
            insights.append(res)
    diagnostics = g.ml_service.get_model_diagnostics()
    return render_template("ml/risk_insights.html", insights=insights, diagnostics=diagnostics)


@ml_bp.route("/predict/<project_id>")
@login_required
def predict(project_id):
    res = g.ml_service.get_project_risk_insights(project_id)
    return jsonify(res)
