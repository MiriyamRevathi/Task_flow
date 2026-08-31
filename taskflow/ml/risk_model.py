"""
TaskFlow Enterprise SaaS - scikit-learn Risk Prediction Model Wrapper.
Implements RandomForestClassifier and GradientBoostingClassifier for local project risk classification:
0 = LOW_RISK
1 = MEDIUM_RISK
2 = HIGH_RISK
"""

from typing import Dict, Any, Tuple, List
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class RiskPredictionModel:
    """scikit-learn Classifier Wrapper for Local Project Risk Assessment."""

    def __init__(self, algorithm: str = "RandomForest"):
        self.algorithm = algorithm
        if algorithm == "GradientBoosting":
            self.model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
        else:
            self.model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
        self.is_trained = False

    def train(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        self.is_trained = True

        y_pred = self.model.predict(X_test)

        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
        rec = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
        f1 = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))

        return {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
        }

    def predict(self, feature_vector: list) -> Tuple[int, float, list]:
        if not self.is_trained:
            return 0, 15.0, [0.8, 0.15, 0.05]

        X_input = np.array(feature_vector).reshape(1, -1)
        pred_class = int(self.model.predict(X_input)[0])
        probabilities = [float(p) for p in self.model.predict_proba(X_input)[0]]

        if len(probabilities) == 3:
            risk_score = round((probabilities[1] * 50.0) + (probabilities[2] * 100.0), 1)
        else:
            risk_score = round(probabilities[0] * 100.0, 1)

        return pred_class, risk_score, probabilities

    def get_feature_importances(self, feature_names: List[str]) -> Dict[str, float]:
        if not self.is_trained or not hasattr(self.model, "feature_importances_"):
            return {}
        importances = self.model.feature_importances_
        res = {name: round(float(imp), 4) for name, imp in zip(feature_names, importances)}
        return dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
