"""
ML Model Registry.
"""

import pickle
from pathlib import Path


class MLModelRegistry:
    @staticmethod
    def save_model(model_obj, filepath: Path):
        with open(filepath, "wb") as f:
            pickle.dump(model_obj, f)

    @staticmethod
    def load_model(filepath: Path):
        if not filepath.exists():
            return None
        with open(filepath, "rb") as f:
            return pickle.load(f)
