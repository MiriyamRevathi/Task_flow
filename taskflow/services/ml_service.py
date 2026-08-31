"""
ML Service Facade.
"""

from typing import Dict, Any, List
from taskflow.ml.training import run_training_pipeline
from taskflow.ml.prediction import MLPredictionEngine
from taskflow.repositories.project_repository import ProjectRepository
from taskflow.repositories.task_repository import TaskRepository


class MLService:
    def __init__(self, project_repo: ProjectRepository, task_repo: TaskRepository):
        self.project_repo = project_repo
        self.task_repo = task_repo
        self.model, self.metrics = run_training_pipeline()
        self.predictor = MLPredictionEngine(self.model)

    def get_project_risk_insights(self, project_id: str) -> Dict[str, Any]:
        proj = self.project_repo.get_by_id(project_id)
        if not proj:
            return {}

        tasks = self.task_repo.get_by_project(project_id)
        res = self.predictor.predict_project_risk(proj, tasks)

        # Update project model risk score
        proj.risk_level = res["risk_level"]
        proj.risk_score = res["risk_score"]
        self.project_repo.save(proj)

        return res

    def get_model_diagnostics(self) -> Dict[str, Any]:
        return {
            "algorithm": self.model.algorithm,
            "metrics": self.metrics,
            "is_trained": self.model.is_trained,
            "feature_count": 9,
        }
