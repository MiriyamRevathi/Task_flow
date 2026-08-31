"""
ML Prediction Engine.
"""

from typing import Dict, Any, List
from taskflow.ml.risk_model import RiskPredictionModel
from taskflow.ml.feature_builder import MLFeatureBuilder
from taskflow.models.project import Project
from taskflow.models.task import Task
from taskflow.models.enums import RiskLevel


class MLPredictionEngine:
    RISK_MAP = {0: RiskLevel.LOW_RISK.value, 1: RiskLevel.MEDIUM_RISK.value, 2: RiskLevel.HIGH_RISK.value}

    def __init__(self, model: RiskPredictionModel):
        self.model = model

    def predict_project_risk(self, project: Project, tasks: List[Task]) -> Dict[str, Any]:
        features = MLFeatureBuilder.extract_project_features(project, tasks)
        pred_class, risk_score, probs = self.model.predict(features)

        risk_level = self.RISK_MAP.get(pred_class, RiskLevel.LOW_RISK.value)

        recommendations = []
        if features[0] > 0.15:
            recommendations.append("High number of overdue tasks detected. Reassign or adjust deadlines.")
        if features[3] > 0.05:
            recommendations.append("Multiple blocked tasks require immediate team lead intervention.")
        if project.is_overdue():
            recommendations.append("Project completion date has passed. Conduct timeline review.")

        if not recommendations:
            recommendations.append("Project timeline and velocity are on track.")

        return {
            "project_id": project.id,
            "project_name": project.name,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "probabilities": probs,
            "feature_vector": features,
            "recommendations": recommendations,
        }
