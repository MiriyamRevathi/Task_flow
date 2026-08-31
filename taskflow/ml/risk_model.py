"""
scikit-learn Risk Prediction Model Wrapper.
Uses RandomForestClassifier and GradientBoostingClassifier for local risk prediction.
"""

from typing import Dict, Any, Tuple
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class RiskPredictionModel:
    def __init__(self, algorithm: str = "RandomForest"):
        self.algorithm = algorithm
        if algorithm == "GradientBoosting":
            self.model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        else:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False

    def train(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        self.is_trained = True

        y_pred = self.model.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

        return {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
        }

    def predict(self, feature_vector: list) -> Tuple[int, float, list]:
        if not self.is_trained:
            # Return fallback if not trained
            return 0, 15.0, [0.8, 0.15, 0.05]

        X_input = np.array(feature_vector).reshape(1, -1)
        pred_class = int(self.model.predict(X_input)[0])
        probabilities = [float(p) for p in self.model.predict_proba(X_input)[0]]
        
        # Calculate continuous 0-100 risk score
        if len(probabilities) == 3:
            risk_score = round((probabilities[1] * 50.0) + (probabilities[2] * 100.0), 1)
        else:
            risk_score = round(probabilities[0] * 100.0, 1)

        return pred_class, risk_score, probabilities
