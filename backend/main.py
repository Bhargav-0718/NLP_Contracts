from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import papermill as pm

app = FastAPI()

# Directories
NOTEBOOK_DIR = "notebooks"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Notebook paths
INPUT_NB = os.path.join(NOTEBOOK_DIR, "input.ipynb")
SUMMARISATION_NB = os.path.join(NOTEBOOK_DIR, "summarisation.ipynb")
REPORT_NB = os.path.join(NOTEBOOK_DIR, "report_generator.ipynb")

@app.post("/upload_contract")
async def upload_contract(file: UploadFile = File(...)):
    # Save uploaded file
    contract_path = os.path.join(OUTPUT_DIR, file.filename)
    with open(contract_path, "wb") as f:
        f.write(await file.read())
    
    try:
        # Step 1: Run classification notebook
        pm.execute_notebook(
            INPUT_NB,
            os.path.join(OUTPUT_DIR, "input_out.ipynb"),
            parameters={"file_path": contract_path}
        )

        # Step 2: Run summarisation notebook
        pm.execute_notebook(
            SUMMARISATION_NB,
            os.path.join(OUTPUT_DIR, "summarisation_out.ipynb"),
            parameters={"file_path": contract_path}
        )

        # Step 3: Run report generation notebook
        pm.execute_notebook(
            REPORT_NB,
            os.path.join(OUTPUT_DIR, "report_out.ipynb"),
        )

        report_path = os.path.join(OUTPUT_DIR, "Contract_Analysis_Report.pdf")
        if os.path.exists(report_path):
            return FileResponse(report_path, filename="Contract_Analysis_Report.pdf", media_type='application/pdf')
        else:
            return {"error": "Report not generated."}

    except Exception as e:
        return {"error": str(e)}
