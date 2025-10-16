# upload_model.py
from huggingface_hub import HfApi
import os

# Hugging Face repo details
repo_id = "bhargav-07-bidkar/Legalbert_Finetuned"  # your HF repo ID
folder_to_upload = "legalbert_finetuned"           # local folder containing your model

# Initialize API
api = HfApi()

# Create repo if it doesn't exist (exist_ok=True avoids errors if it already exists)
try:
    api.create_repo(repo_id=repo_id, repo_type="model", exist_ok=True)
    print(f"Repo '{repo_id}' is ready.")
except Exception as e:
    print("Error while creating repo:", e)

# Upload folder to Hugging Face
print(f"Uploading folder '{folder_to_upload}' to '{repo_id}'...")
api.upload_folder(
    folder_path=folder_to_upload,
    repo_id=repo_id,
    repo_type="model",
    path_in_repo="",        # keep folder contents at the root of the repo
    ignore_patterns=["*.log", "__pycache__/", ".git/"]
)

print(f"Upload finished! Verify at: https://huggingface.co/{repo_id}")
