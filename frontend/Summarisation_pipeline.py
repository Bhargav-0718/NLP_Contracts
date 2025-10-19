import os
import re
import pdfplumber
from docx import Document
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------- Text Extraction -------------------- #
def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(docx_path: str) -> str:
    doc = Document(docx_path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

# -------------------- OpenAI Summarization -------------------- #
SUMMARIZATION_PROMPT = """
You are a legal summarization assistant. Given the contract clause(s) below, create a concise, abstractive legal summary.
Focus on: parties, effective/expiration dates, termination rights, payment/compensation obligations, liability caps, indemnities, IP ownership/licensing, exclusivity, and any unusual risks.
Keep the answer concise (about 3-6 sentences) and use plain language but preserve legal facts and numeric values.

Clause(s):
{chunk_text}

Provide:
1) A short 1-2 sentence overview.
2) Bullet list of top 4 obligations / risks with short tags (e.g., TERMINATION: either party may..., LIABILITY CAP: $X...).
3) If present, list any key dates or numeric amounts found.
"""

def summarize_chunk_openai(chunk_text: str, model: str = "gpt-4.1-mini", temperature: float = 0.0, max_tokens: int = 400) -> str:
    prompt = SUMMARIZATION_PROMPT.format(chunk_text=chunk_text)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful legal assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return resp.choices[0].message.content.strip()

def hierarchical_summary_openai(text: str, chunk_size_chars: int = 2500, overlap_chars: int = 200, model="gpt-4.1-mini"):
    text = re.sub(r'\n{2,}', '\n\n', text).strip()
    
    # Split text into overlapping chunks
    chunks = []
    i = 0
    while i < len(text):
        chunk = text[i:i+chunk_size_chars]
        chunks.append(chunk)
        i += chunk_size_chars - overlap_chars

    # Summarize each chunk
    chunk_summaries = []
    for ch in chunks:
        summary = summarize_chunk_openai(ch, model=model)
        chunk_summaries.append(summary)

    # Combine summaries and produce final summary
    combined = "\n\n".join(chunk_summaries)
    final_prompt = (
        "You are a legal summarization assistant. The following are intermediate summaries "
        "of parts of a contract. Produce a single concise abstractive summary of the whole contract, "
        "emphasizing obligations, risks, and important dates and numeric values. "
        "Also produce a short (4-item) prioritized checklist of clauses that require human review.\n\n"
        f"{combined}"
    )

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful legal assistant."},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.0,
        max_tokens=600
    )
    final_summary = resp.choices[0].message.content.strip()
    return final_summary, chunk_summaries

# -------------------- Main Function -------------------- #
def summarize_contract(file_path: str, output_path: str = None) -> str:
    """
    Summarize a contract file (PDF or DOCX) and save the abstractive summary.
    
    Args:
        file_path (str): Path to the uploaded contract file
        output_path (str, optional): Path to save the summary. Defaults to 'Contract_Abstractive_Summary.txt' in current folder.
    
    Returns:
        str: Final abstractive summary
    """
    # Extract text
    if file_path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type")

    # Summarize
    final_summary, _ = hierarchical_summary_openai(text)

    # Set default output path if none provided
    if output_path is None:
        output_path = os.path.join(os.path.dirname(file_path), "Contract_Abstractive_Summary.txt")

    # Save summary
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_summary)

    print(f"✅ Abstractive summary saved to '{output_path}'")
    return final_summary
