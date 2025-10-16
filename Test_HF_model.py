from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Replace with your repo ID
repo_id = "bhargav-07-bidkar/Legalbert_Finetuned"

# Load tokenizer and model directly from Hugging Face
tokenizer = AutoTokenizer.from_pretrained(repo_id)
model = AutoModelForSequenceClassification.from_pretrained(repo_id)

# Example usage
text = "This is a sample contract clause."
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)
print(outputs)
