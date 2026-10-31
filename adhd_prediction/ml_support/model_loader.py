import joblib
import os
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, "ml_models", "adhd_random_forest_model_v2.pkl")

_model = None

def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model