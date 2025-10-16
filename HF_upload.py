from huggingface_hub import HfApi
import os

repo_id = "bhargav-07-bidkar/Legalbert_Finetuned"
folder_to_upload = "legalbert_finetuned"

api = HfApi()

def upload_folder_in_batches(folder):
    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        if os.path.isdir(item_path):
            # Upload each checkpoint folder as a batch
            print(f"Uploading folder: {item}")
            for root, _, files in os.walk(item_path):
                for f in files:
                    file_path = os.path.join(root, f)
                    relative_path = os.path.relpath(file_path, folder)
                    api.upload_file(
                        path_or_fileobj=file_path,
                        path_in_repo=relative_path,
                        repo_id=repo_id,
                        repo_type="model"
                    )
        else:
            # Upload root-level files
            print(f"Uploading file: {item}")
            api.upload_file(
                path_or_fileobj=item_path,
                path_in_repo=item,
                repo_id=repo_id,
                repo_type="model"
            )

upload_folder_in_batches(folder_to_upload)
print(f"Upload finished! Check at https://huggingface.co/{repo_id}")
