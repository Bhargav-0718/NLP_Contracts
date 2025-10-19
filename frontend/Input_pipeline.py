# backend/input_processor.py

import re
import torch
import joblib
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pdfplumber
from docx import Document
import os

# -------------------------
# Config: Paths
# -------------------------
MODEL_PATH = ("D:\AI\Projects\Contract_NLP\legalbert_finetuned")
LABEL_ENCODER_PATH = ("D:\AI\Projects\Contract_NLP\label_encoder.pkl")
OUTPUT_CSV_PATH = ("D:\AI\Projects\Contract_NLP\output\classified_contract.csv")

# -------------------------
# Text extraction
# -------------------------
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def split_into_clauses(text):
    clauses = re.split(r'\n\d+\.|\n\d+\)|\n•|\n-|\n\n', text)
    return [c.strip() for c in clauses if len(c.strip()) > 20]

# -------------------------
# Load model and label encoder
# -------------------------
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()
le = joblib.load(LABEL_ENCODER_PATH)

# -------------------------
# Prediction
# -------------------------
def predict_clause_label(clause):
    inputs = tokenizer(clause, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        pred_id = torch.argmax(outputs.logits, dim=-1).item()
    return le.inverse_transform([pred_id])[0], pred_id

def classify_contract(file_path, output_csv=OUTPUT_CSV_PATH):
    if file_path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type")

    clauses = split_into_clauses(text)

    label_id_to_tier = {
        0: 5, 1: 5, 2: 5, 3: 5, 4: 1, 5: 1, 6: 1, 7: 3, 8: 2, 9: 2,
        10: 5, 11: 5, 12: 5, 13: 1, 14: 5, 15: 5, 16: 1, 17: 1, 18: 2,
        19: 2, 20: 2, 21: 2, 22: 1, 23: 2, 24: 2, 25: 2, 26: 2, 27: 1,
        28: 2, 29: 2, 30: 4, 31: 4, 32: 5, 33: 5, 34: 2, 35: 2, 36: 4,
        37: 3, 38: 3, 39: 2, 40: 2, 41: 1, 42: 4, 43: 1, 44: 2, 45: 2, 46: 3
    }

    results = []
    for clause in clauses:
        label, pred_id = predict_clause_label(clause)
        tier = label_id_to_tier.get(pred_id, 5)
        results.append({
            "predicted_class_id": pred_id,
            "Predicted Label": label,
            "Tier": tier,
            "Clause": clause
        })

    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"✅ Classification complete. Saved to '{output_csv}'")
    return df
