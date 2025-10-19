# backend/services/nlp_pipeline.py
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

class NLPPipeline:
    def __init__(self, model_path="nlpaueb/legal-bert-base-uncased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def classify_clause(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = self.model(**inputs).logits
        pred_id = torch.argmax(logits, dim=-1).item()
        return int(pred_id)

    def summarize_text(self, text: str):
        summary = self.summarizer(text, max_length=200, min_length=50, do_sample=False)
        return summary[0]["summary_text"]
