"""
ML Model Metadata Domain Model.
Stores model performance metrics, feature importance scores, training timestamps, and algorithm versions.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, List


class MLModelMeta:
    def __init__(
        self,
        id: str,
        name: str,
        algorithm: str,
        version: str,
        accuracy: float,
        precision: float,
        recall: float,
        f1_score: float,
        feature_names: List[str],
        feature_importances: Dict[str, float],
        dataset_sample_size: int,
        trained_at: Optional[str] = None,
        model_filepath: str = "",
        is_active: bool = True,
    ):
        self.id = id
        self.name = name
        self.algorithm = algorithm
        self.version = version
        self.accuracy = float(accuracy)
        self.precision = float(precision)
        self.recall = float(recall)
        self.f1_score = float(f1_score)
        self.feature_names = feature_names or []
        self.feature_importances = feature_importances or {}
        self.dataset_sample_size = dataset_sample_size
        self.trained_at = trained_at or datetime.now(timezone.utc).isoformat()
        self.model_filepath = model_filepath
        self.is_active = is_active

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "algorithm": self.algorithm,
            "version": self.version,
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score,
            "feature_names": self.feature_names,
            "feature_importances": self.feature_importances,
            "dataset_sample_size": self.dataset_sample_size,
            "trained_at": self.trained_at,
            "model_filepath": self.model_filepath,
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MLModelMeta":
        return cls(
            id=data["id"],
            name=data["name"],
            algorithm=data.get("algorithm", "RandomForest"),
            version=data.get("version", "1.0.0"),
            accuracy=data.get("accuracy", 0.0),
            precision=data.get("precision", 0.0),
            recall=data.get("recall", 0.0),
            f1_score=data.get("f1_score", 0.0),
            feature_names=data.get("feature_names", []),
            feature_importances=data.get("feature_importances", {}),
            dataset_sample_size=data.get("dataset_sample_size", 0),
            trained_at=data.get("trained_at"),
            model_filepath=data.get("model_filepath", ""),
            is_active=data.get("is_active", True),
        )
