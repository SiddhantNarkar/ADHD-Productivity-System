import pandas as pd
from .model_loader import get_model

FEATURE_COLUMNS = [
    "age",
    "age_group",
    "inattention_pct",
    "hyperactivity_pct",
    "impulsivity_pct",
    "impairment_flag",
    "attention_accuracy",
    "false_press_rate",
    "reaction_time_ms",
    "reaction_time_variability",
    "level1_score",
    "level2_score",
    "level3_score",
    "memory_drop",
    "avg_completion_time_sec"
]

def predict_severity(feature_vector):

    model = get_model()

    df = pd.DataFrame(feature_vector, columns=FEATURE_COLUMNS)

    prediction = model.predict(df)[0]
    probabilities = model.predict_proba(df)[0]

    confidence = max(probabilities)

    return {
        "severity_level": int(prediction),
        "confidence": float(confidence),
        "probabilities": probabilities.tolist()
    }