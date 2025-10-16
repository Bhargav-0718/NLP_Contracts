import torch
import joblib
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# -----------------------------
# 1. Load fine-tuned model
# -----------------------------
model_path = "./legalbert_finetuned"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.eval()

# -----------------------------
# 2. Load label encoder
# -----------------------------
# This must have been saved during training:
# joblib.dump(le, "label_encoder.pkl")
le = joblib.load("label_encoder.pkl")

# -----------------------------
# 3. Test clauses
# -----------------------------
test_clauses = [
    "Either party may terminate this Agreement upon thirty (30) days notice.",
    "The Supplier shall indemnify and hold harmless the Buyer against all claims.",
    "This Agreement shall be governed by the laws of the State of New York."
]

for clause in test_clauses:
    # Tokenize
    inputs = tokenizer(clause, return_tensors="pt", truncation=True, padding=True, max_length=512)

    # Predict
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_id = torch.argmax(logits, dim=-1).item()

    # Map back to original label
    predicted_label = le.inverse_transform([predicted_class_id])[0]

    print(f"\nClause: {clause}")
    print(f"Predicted Class ID: {predicted_class_id}")
    print(f"Predicted Label: {predicted_label}")
