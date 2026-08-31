"""
ML Training Pipeline Executable.
"""

from taskflow.ml.dataset_generator import MLDatasetGenerator
from taskflow.ml.risk_model import RiskPredictionModel


def run_training_pipeline() -> Tuple[RiskPredictionModel, Dict[str, float]]:
    X, y = MLDatasetGenerator.generate_training_data(500)
    model = RiskPredictionModel(algorithm="RandomForest")
    metrics = model.train(X, y)
    return model, metrics
