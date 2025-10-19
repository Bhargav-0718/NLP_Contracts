import joblib
import pandas as pd

# Load the saved LabelEncoder
le = joblib.load("label_encoder.pkl")

# View label -> ID mapping
label_mapping = dict(zip(le.classes_, range(len(le.classes_))))
print("Label to ID mapping:")
for label, idx in label_mapping.items():
    print(f"{label} -> {idx}")
