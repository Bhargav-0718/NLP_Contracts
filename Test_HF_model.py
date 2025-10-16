import torch
import joblib
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# -----------------------------
# 1. Load model from Hugging Face
# -----------------------------
repo_id = "bhargav-07-bidkar/Legalbert_Finetuned"
tokenizer = AutoTokenizer.from_pretrained(repo_id)
model = AutoModelForSequenceClassification.from_pretrained(repo_id)
model.eval()

# -----------------------------
# 2. Load LabelEncoder
# -----------------------------
# Make sure label_encoder.pkl is in the same directory as this script
le = joblib.load("label_encoder.pkl")

# -----------------------------
# 3. Sample clauses
# -----------------------------
sample_clauses = [
    "Either party may terminate this Agreement upon thirty (30) days notice.",
    "The Supplier shall indemnify and hold harmless the Buyer against all claims.",
    "This Agreement shall be governed by the laws of the State of New York.",
    "All payments must be made within thirty (30) days from invoice receipt.",
    "The Receiving Party shall maintain strict confidentiality of all disclosed information.",
    "The Contractor agrees to deliver the services by the agreed deadlines.",
    "In the event of a breach, the non-breaching party may seek remedies available at law."
]

# -----------------------------
# 4. Predict labels
# -----------------------------
for clause in sample_clauses:
    # Tokenize
    inputs = tokenizer(clause, return_tensors="pt", truncation=True, padding=True, max_length=512)

    # Predict
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_id = torch.argmax(logits, dim=-1).item()

    # Convert class ID to human-readable label
    predicted_label = le.inverse_transform([predicted_class_id])[0]

    print(f"\nClause: {clause}")
    print(f"Predicted Class ID: {predicted_class_id}")
    print(f"Predicted Label: {predicted_label}")
