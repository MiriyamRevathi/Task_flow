"""
ML Model Evaluation Metrics.
"""

def evaluate_model_performance(metrics: dict) -> str:
    return f"Model Accuracy: {metrics.get('accuracy', 0)*100}% | F1 Score: {metrics.get('f1_score', 0)}"
