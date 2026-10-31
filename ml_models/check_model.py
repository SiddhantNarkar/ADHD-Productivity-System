import joblib

model = joblib.load("adhd_random_forest_model_v2.pkl")

print("\n===== ADHD MODEL INFORMATION =====")
print("\n1.Model Type:")
print(type(model))

# Print basic information
print("\n2.Loaded Model:")
print(model)

# Model parameters
try:
    print("\nModel Parameters:")
    for key, value in model.get_params().items():
        print(f"{key} : {value}")
except:
    print("\nModel parameters not available")

print("\n===== MODEL LOADED SUCCESSFULLY =====")