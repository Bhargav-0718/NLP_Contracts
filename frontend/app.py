# app.py
import streamlit as st
import requests
from pathlib import Path
import os
# Backend API URL
API_URL = "http://127.0.0.1:8000/upload_contract"

st.set_page_config(page_title="Contract NLP Analyzer", layout="centered")

st.title("📄 Contract Summarization & Analysis")
st.write(
    "Upload your contract (PDF or DOCX) and get a comprehensive analysis report with clause tiers and summaries."
)

# File upload
uploaded_file = st.file_uploader("Upload a Contract", type=["pdf", "docx"])
if uploaded_file is not None:
    save_path = os.path.join("D:/AI/Projects/Contract_NLP/backend/output", uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File saved at: {save_path}")

    
    if st.button("Generate Report"):
        with st.spinner("Processing contract... this may take a while ⏳"):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            try:
                response = requests.post(API_URL, files=files)
                if response.status_code == 200:
                    # Save the PDF locally for download
                    output_path = Path("Contract_Analysis_Report.pdf")
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    
                    st.success("✅ Report generated successfully!")
                    st.download_button(
                        label="📥 Download Contract Analysis PDF",
                        data=open(output_path, "rb").read(),
                        file_name="Contract_Analysis_Report.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error(f"Error from backend: {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
