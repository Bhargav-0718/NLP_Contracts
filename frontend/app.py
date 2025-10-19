import streamlit as st
import os
from Input_pipeline import classify_contract
from Summarisation_pipeline import hierarchical_summary_openai
from Report_Generator import generate_pdf_report

# -----------------------------
# Setup paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = ("D:\AI\Projects\Contract_NLP\output")

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

st.set_page_config(page_title="Contract NLP Tool", layout="wide")
st.title("📄 Contract NLP Tool")

# -----------------------------
# File upload
# -----------------------------
uploaded_file = st.file_uploader("Upload your contract (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    uploaded_file_path = os.path.join(UPLOADS_DIR, uploaded_file.name)
    with open(uploaded_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"File uploaded: {uploaded_file.name}")

    # -----------------------------
    # Step 1: Clause Classification
    # -----------------------------
    st.subheader("Step 1: Classifying Contract Clauses...")
    try:
        classified_df = classify_contract(uploaded_file_path)
        st.success("✅ Clause classification complete!")
        st.dataframe(classified_df.head())

        csv_path = os.path.join(OUTPUT_DIR, "classified_contract.csv")
        st.download_button(
            label="Download Classified CSV",
            data=open(csv_path, "rb"),
            file_name="classified_contract.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"Error during classification: {e}")

    # -----------------------------
    # Step 2: Summarization
    # -----------------------------
    st.subheader("Step 2: Generating Contract Summary...")
    try:
        final_summary, chunk_summaries = hierarchical_summary_openai(
            text=classified_df['Clause'].str.cat(sep="\n"),
            chunk_size_chars=2500,
            overlap_chars=200
        )
        summary_path = os.path.join(OUTPUT_DIR, "Contract_Abstractive_Summary.txt")
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(final_summary)
        st.success("✅ Summary generated!")
        st.text_area("Contract Summary", final_summary, height=300)

        st.download_button(
            label="Download Summary",
            data=open(summary_path, "rb"),
            file_name="Contract_Abstractive_Summary.txt",
            mime="text/plain"
        )
    except Exception as e:
        st.error(f"Error during summarization: {e}")

    # -----------------------------
    # Step 3: Generate PDF Report
    # -----------------------------
    st.subheader("Step 3: Generating PDF Report...")
    try:
        pdf_path = os.path.join(OUTPUT_DIR, "Contract_Analysis_Report.pdf")
        generate_pdf_report(
            csv_path=os.path.join(OUTPUT_DIR, "classified_contract.csv"),
            summary_path=summary_path,
            output_pdf=pdf_path,
            graphs_dir="D:\AI\Projects\Contract_NLP\Graphs"
        )
        st.success(f"✅ PDF report generated: {pdf_path}")

        st.download_button(
            label="Download PDF Report",
            data=open(pdf_path, "rb"),
            file_name="Contract_Analysis_Report.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Error during PDF generation: {e}")
