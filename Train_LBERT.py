# LegalBERT_Paragraph_Classification.py
import os
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm

# -------------------------------
# Paths and Hyperparameters
# -------------------------------
MODEL_NAME = "nlpaueb/legal-bert-base-uncased"
DATA_DIR = "CUAD_v1/processed"
TRAIN_CSV = os.path.join(DATA_DIR, "train_clauses.csv")
VAL_CSV = os.path.join(DATA_DIR, "validation_clauses.csv")
TEST_CSV = os.path.join(DATA_DIR, "test_clauses.csv")
BATCH_SIZE = 8
EPOCHS = 3
LR = 2e-5
MAX_LEN = 512  # max tokens per paragraph

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -------------------------------
# Dataset Class
# -------------------------------
class CUADDataset(Dataset):
    def __init__(self, clauses, paragraphs, labels, tokenizer, max_len=512):
        self.clauses = clauses
        self.paragraphs = paragraphs
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.clauses)

    def __getitem__(self, idx):
        clause = str(self.clauses[idx])
        paragraph = str(self.paragraphs[idx])
        text = f"{clause} [SEP] {paragraph}"  # Combine clause + paragraph

        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_tensors="pt",
        )
        item = {key: val.squeeze(0) for key, val in encoding.items()}
        item["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item

# -------------------------------
# Load CSVs and encode labels
# -------------------------------
def load_data(train_csv, val_csv, test_csv):
    train_df = pd.read_csv(train_csv)
    val_df = pd.read_csv(val_csv)
    test_df = pd.read_csv(test_csv)

    # Encode labels
    le = LabelEncoder()
    all_labels = pd.concat([train_df['label'], val_df['label'], test_df['label']])
    le.fit(all_labels)

    train_df['label'] = le.transform(train_df['label'])
    val_df['label'] = le.transform(val_df['label'])
    test_df['label'] = le.transform(test_df['label'])

    return train_df, val_df, test_df, le

# -------------------------------
# Data Loaders
# -------------------------------
def create_dataloaders(tokenizer, train_df, val_df, test_df, batch_size):
    train_dataset = CUADDataset(train_df['clause'], train_df['paragraph'], train_df['label'], tokenizer, max_len=MAX_LEN)
    val_dataset = CUADDataset(val_df['clause'], val_df['paragraph'], val_df['label'], tokenizer, max_len=MAX_LEN)
    test_dataset = CUADDataset(test_df['clause'], test_df['paragraph'], test_df['label'], tokenizer, max_len=MAX_LEN)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, test_loader

# -------------------------------
# Training Loop
# -------------------------------
def train(model, dataloader, optimizer):
    model.train()
    total_loss = 0
    for batch in tqdm(dataloader, desc="Training"):
        batch = {k: v.to(DEVICE) for k, v in batch.items()}
        outputs = model(**batch)
        loss = outputs.loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(dataloader)

def evaluate(model, dataloader):
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Evaluating"):
            batch = {k: v.to(DEVICE) for k, v in batch.items()}
            outputs = model(**batch)
            loss = outputs.loss
            logits = outputs.logits
            total_loss += loss.item()
            preds = torch.argmax(logits, dim=-1)
            correct += (preds == batch['labels']).sum().item()
            total += batch['labels'].size(0)
    accuracy = correct / total
    return total_loss / len(dataloader), accuracy

# -------------------------------
# Main
# -------------------------------
def main():
    # Load data
    train_df, val_df, test_df, le = load_data(TRAIN_CSV, VAL_CSV, TEST_CSV)
    print(f"Labels: {list(le.classes_)}")
    print(f"Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")

    # Tokenizer & Model
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=len(le.classes_))
    model.to(DEVICE)

    # Data loaders
    train_loader, val_loader, test_loader = create_dataloaders(tokenizer, train_df, val_df, test_df, BATCH_SIZE)

    # Optimizer
    optimizer = AdamW(model.parameters(), lr=LR)

    # Training
    for epoch in range(EPOCHS):
        print(f"\nEpoch {epoch+1}/{EPOCHS}")
        train_loss = train(model, train_loader, optimizer)
        val_loss, val_acc = evaluate(model, val_loader)
        print(f"Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.4f}")

    # Test evaluation
    test_loss, test_acc = evaluate(model, test_loader)
    print(f"\nTest Loss: {test_loss:.4f} | Test Acc: {test_acc:.4f}")

    # Save model
    model_save_path = "legalbert_cuad_paragraph"
    os.makedirs(model_save_path, exist_ok=True)
    model.save_pretrained(model_save_path)
    tokenizer.save_pretrained(model_save_path)
    print(f"Model saved to {model_save_path}")

if __name__ == "__main__":
    main()
# ------------------------