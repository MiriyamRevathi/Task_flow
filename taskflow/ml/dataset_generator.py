"""
ML Dataset Generator.
Generates synthetic project training samples with realistic risk labels (LOW, MEDIUM, HIGH) for local ML training.
"""

from typing import Tuple, List
import numpy as np


class MLDatasetGenerator:
    @classmethod
    def generate_training_data(cls, num_samples: int = 500) -> Tuple[np.ndarray, np.ndarray]:
        np.random.seed(42)
        
        # Features: [overdue_ratio, completion_velocity, backlog_ratio, blocked_ratio, avg_hours, delay_ratio, capacity, age, remaining]
        overdue_ratio = np.random.beta(a=1.5, b=5, size=num_samples)
        velocity = np.random.uniform(0.1, 0.95, size=num_samples)
        backlog_ratio = np.random.uniform(0.1, 0.7, size=num_samples)
        blocked_ratio = np.random.beta(a=1, b=8, size=num_samples)
        avg_hours = np.random.exponential(scale=15.0, size=num_samples)
        delay_ratio = np.random.uniform(0.0, 0.5, size=num_samples)
        capacity = np.random.uniform(10.0, 100.0, size=num_samples)
        age = np.random.uniform(5.0, 180.0, size=num_samples)
        remaining = np.random.uniform(1.0, 50.0, size=num_samples)

        X = np.column_stack([
            overdue_ratio, velocity, backlog_ratio, blocked_ratio,
            avg_hours, delay_ratio, capacity, age, remaining
        ])

        # Generate target risk labels: 0=LOW_RISK, 1=MEDIUM_RISK, 2=HIGH_RISK
        risk_score = (overdue_ratio * 0.45) + (blocked_ratio * 0.35) + (delay_ratio * 0.20) - (velocity * 0.25)
        
        y = np.zeros(num_samples, dtype=int)
        y[risk_score > 0.15] = 1  # MEDIUM_RISK
        y[risk_score > 0.35] = 2  # HIGH_RISK

        return X, y
