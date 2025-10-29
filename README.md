# 📜 NLP Contract Summarization & Tier-wise Clause Review

This project presents an **NLP-powered framework** for **automated contract summarization** and **tier-wise clause classification**, helping legal professionals and organizations efficiently interpret and prioritize contractual information.  
By leveraging transformer-based models such as **Legal-BERT**, and **OpenAI**, the system identifies, categorizes, and summarizes clauses to enhance accuracy, speed, and strategic decision-making in contract analysis.

---

## 🚀 Project Overview

Manual contract review is often **slow, repetitive, and complex**, requiring domain expertise to evaluate hundreds of clauses per agreement.  
This project automates that process by:

- **Extracting clauses** from PDF/DOCX contracts.  
- **Classifying each clause** using Legal-BERT into predefined categories.  
- **Assigning Tier levels (1–5)** based on clause criticality and review priority.  
- **Generating concise, abstractive summaries** using OpenAI GPT 4.1-mini.  
- **Producing structured reports and CSV outputs** for downstream legal workflows.

The end goal is to streamline legal document review and enable faster, tier-based contract understanding.

---

## 🧩 Problem Statement

Contract review teams often face challenges such as:

- Large volumes of lengthy contracts with inconsistent structures.  
- Difficulty identifying key obligations and conditions quickly.  
- Time-intensive manual analysis requiring specialized expertise.  
- The need for standardized prioritization of clauses.  

This project addresses these issues by combining **Legal NLP** and **Generative AI** to automatically extract, summarize, and categorize contractual content, supporting efficient legal review and prioritization.

---

## 📚 Literature Review

Several research efforts and datasets have contributed to the advancement of **legal NLP** tasks such as clause classification, contract understanding, and summarization. Key references include:

| Dataset / Benchmark | Description | Links |
|----------------------|-------------|--------|
| **CUAD (Contract Understanding Atticus Dataset)** | 510 contracts with ~13K annotated clauses across 41 clause types for contract understanding. | [Paper](https://arxiv.org/abs/2103.06268) • [GitHub](https://github.com/TheAtticusProject/cuad) |
| **MAUD (Merger Agreement Understanding Dataset)** | Clause-level question answering in merger agreements. | [Paper](https://arxiv.org/html/2301.00876) |
| **LexGLUE / LEDGAR** | Large-scale legal document classification from SEC filings. | [Paper](https://aclanthology.org/2022.acl-long.297.pdf) |
| **LegalBench** | Benchmark for evaluating legal reasoning in LLMs. | [Paper](https://arxiv.org/abs/2308.11462) |
| **ACORD** | Dataset for clause retrieval and document drafting workflows. | — |

These benchmarks guided the design of our clause classification and summarization pipelines.

---

## 📂 Dataset Details

This project primarily utilizes the **CUAD dataset**, which provides high-quality, expert-labeled contract data.

**Dataset Specifications:**
- **510 commercial contracts**
- **13,000+ annotated clauses**
- **41 clause types** (e.g., Termination, Liability, Indemnification, IP Ownership)
- **Mapped to 5 review tiers** for prioritization

The dataset enables fine-tuning of both classification and summarization models for realistic legal document workflows.

---

## ⚙️ Preprocessing Pipeline

### 🧾 Early Data Aggregation

The original CUAD dataset was distributed as **~30 separate CSV files**, each corresponding to a distinct clause type (e.g., *Termination.csv*, *Liability.csv*, *Indemnification.csv*).  
Each file contained clause-level annotations with the following columns:
- **Contract Name**
- **Clause Text**
- **Clause Type**

To streamline training and simplify downstream processing, these CSVs were **consolidated into a unified dataset:**

> ✅ **`combined_clauses.csv`**

**Steps for Aggregation:**
1. Loaded all individual CSV files using `pandas`.  
2. Added a `label` column representing the clause type derived from the filename.  
3. Concatenated all dataframes into a single structure.  
4. Normalized text by removing duplicates, newlines, and extra spaces.  
5. Saved the combined corpus as `combined_clauses.csv` containing:  
   ```
   [Clause Text, Label]
   ```

This unified dataset serves as the foundational input for clause classification and tier assignment.

---

### 🧮 Text Preprocessing Steps

Once unified, the following text processing pipeline was applied:

1. **Text Extraction** — Extracted text from PDFs using `pdfplumber` and DOCX files using `python-docx`.  
2. **Segmentation** — Divided contracts into **clauses** and **paragraphs** based on linguistic cues and punctuation.  
3. **Cleaning** — Removed headers, footers, numbering, and redundant whitespace.  
4. **Label Mapping** — Mapped CUAD clause labels to standardized labels for consistency.  
5. **Tier Assignment** — Assigned each label to one of five predefined Tiers for review prioritization.

---

## 🧠 Model Architecture

### 1. **Clause Classification**
- **Model:** [Legal-BERT](https://huggingface.co/nlpaueb/legal-bert-base-uncased)  
- **Objective:** Classify clauses into predefined clause types and assign them a Tier.  
- **Output:** `(Clause Text → Label → Tier)`

### 2. **Contract Summarization**
- **Models:** [GPT-4.1-mini](https://platform.openai.com/docs/models#gpt-4-1-mini)
- **Objective:** Generate **abstractive summaries** capturing the key points of the entire contract or selected tiers.  
- **Output:** Coherent, domain-aware summaries suitable for professional review.

### 3. **Integration**
- Combined pipeline produces a **tiered summary** for each contract, linking clause predictions to summarization output.

---

## 🏷️ Tier System

Clauses are categorized into **five Tiers** based on their importance, contractual implications, and review priority.

| **Tier** | **Description** | **Typical Clauses (Examples)** |
|-----------|-----------------|-------------------------------|
| **Tier 1 — Critical** | Core clauses that significantly influence contractual terms; require top-priority review. | Termination, Liability, IP Ownership, Governing Law, Exclusivity |
| **Tier 2 — Important** | Clauses defining major obligations or constraints that should be reviewed carefully. | Non-Compete, Indemnification, Insurance, Joint IP Ownership |
| **Tier 3 — Moderate** | Common operational clauses; generally standard but may vary across contracts. | Warranty Duration, Renewal Terms |
| **Tier 4 — Low** | Administrative or procedural clauses that seldom require in-depth analysis. | Notice Periods, Third-Party Beneficiary |
| **Tier 5 — Trivial / Informational** | Basic document-level metadata and boilerplate elements. | Effective Date, Parties, Document Name |

---

## 📊 Training & Evaluation

**Setup**
- Fine-tuned **Legal-BERT** on the `combined_clauses.csv` dataset.  
- Evaluated on held-out clauses using **Accuracy** and **F1 Score** metrics.  
- Conducted experiments on GPU (A100/RTX-class hardware).

**Outcomes**
- Consistent clause labeling performance across all 41 clause types.  
- Robust generalization to unseen contract structures.  
- High interpretability through tier-wise clause visualization.

---

## 📝 Output & Reporting

**Outputs Produced:**
- **CSV:**  
  `Clause | Predicted_Label | Tier `  
- **Tier-based Filtering:**  
  View or export specific tiers for focused review.  
- **Summarization:**  
  Abstractive summaries generated using OpenAI GPT 4.1-mini.  
- **PDF Reports:**  
  Containing tier distribution charts, clause summaries, and contract overviews.

---

## 📈 Interpretation & Impact

- **Efficiency:** Automates repetitive clause review tasks.  
- **Prioritization:** Enables structured review via tiering.  
- **Scalability:** Adapts to multiple contract domains and volumes.  
- **Practicality:** Easily integrates with contract management systems or AI-assisted review dashboards.

---

## 🔮 Future Directions

- Expansion to multilingual contracts and international law corpora.  
- Incorporation of contextual retrieval (using ACORD dataset).  
- Integration with interactive review dashboards for real-time clause analysis.  
- Extension to clause revision and negotiation assistance.

---
