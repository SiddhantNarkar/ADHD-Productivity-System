import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset from ml_model folder
df = pd.read_csv("ml_models/adhd_synthetic_20000_v2.csv")

X = df.drop(columns=["severity_level"])
y = df["severity_level"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    stratify=y,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=14,
    min_samples_split=15,
    min_samples_leaf=8,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Save model back to ml_model folder
joblib.dump(model, "ml_models/adhd_random_forest_model_v2.pkl")

print("✅ Model retrained successfully with current sklearn version.")