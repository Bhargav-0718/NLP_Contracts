# 📜 NLP Contract Summarization & Tier-wise Clause Review  

This project presents an **NLP-powered framework** for automated contract summarization and **tier-wise clause classification**, designed to help legal professionals and organizations efficiently interpret and prioritize contractual information.  

By leveraging transformer-based models such as **Legal-BERT** and **OpenAI GPT-4.1-mini**, the system identifies, categorizes, and summarizes contractual clauses — enhancing **accuracy, speed, and decision-making** in legal document analysis.  

---

## 🚀 Project Overview  

Manual contract review is often slow, repetitive, and complex, requiring domain expertise to evaluate hundreds of clauses per agreement.  
This project automates that process through the following key steps:  

- 🧾 **Clause Extraction** from PDF/DOCX contracts.  
- 🧠 **Classification** of each clause using a fine-tuned Legal-BERT model into predefined categories.  
- 🏷️ **Tier Assignment** (1–5) based on clause criticality and review priority.  
- ✍️ **Summarization** using GPT-4.1-mini to produce concise, abstractive summaries.  
- 📊 **Report Generation** in CSV and PDF formats for structured downstream legal workflows.  

The goal is to **streamline legal document review**, enabling faster and more consistent tier-based understanding of contractual information.  

---

## 🧩 Problem Statement  

Contract review teams often face major challenges such as:  
- Large volumes of lengthy, inconsistently formatted contracts.  
- Difficulty in quickly identifying key obligations and risk-bearing clauses.  
- Time-intensive manual analysis requiring specialized legal expertise.  
- Lack of standardized prioritization mechanisms for clause importance.  

This project addresses these problems by combining **Legal NLP** and **Generative AI** to automatically extract, classify, and summarize contractual content, creating a structured and prioritized workflow for legal review.  

---

## 📚 Literature Review  

Several benchmark datasets have shaped progress in Legal NLP, particularly in clause classification and contract understanding.  

| Dataset / Benchmark | Description | Links |
|---------------------|--------------|-------|
| **CUAD (Contract Understanding Atticus Dataset)** | 510 contracts with ~13K annotated clauses across 41 clause types for contract understanding. | Paper • GitHub |
| **MAUD (Merger Agreement Understanding Dataset)** | Clause-level question answering in merger agreements. | Paper |
| **LexGLUE / LEDGAR** | Large-scale legal document classification from SEC filings. | Paper |
| **LegalBench** | Benchmark for evaluating legal reasoning in LLMs. | Paper |
| **ACORD** | Dataset for clause retrieval and document drafting workflows. | — |

These benchmarks inspired the design of the project’s **clause classification and summarization pipeline**.  

---

## 📂 Dataset Details  

The project primarily utilizes the **CUAD dataset**, which provides high-quality, expert-labeled contract data.  

**Specifications:**  
- 510 commercial contracts  
- 13,000+ annotated clauses  
- 41 clause types (e.g., Termination, Liability, IP Ownership, Indemnification)  
- Each mapped to one of **five review tiers** for prioritization  

This dataset supports **fine-tuning** of both classification and summarization models for realistic, domain-specific contract workflows.  

---

## ⚙️ Preprocessing Pipeline  

### 🧾 Early Data Aggregation  
The CUAD dataset was originally distributed as ~30 clause-specific CSV files (e.g., *Termination.csv*, *Liability.csv*).  
To simplify training, these were consolidated into a single dataset — **combined_clauses.csv** — containing two key columns:  
`[Clause Text, Label]`  

**Steps:**  
1. Loaded all CSVs using `pandas`.  
2. Added a `label` column based on filename.  
3. Concatenated and cleaned the text (duplicates, newlines, whitespace).  
4. Saved as **combined_clauses.csv**, forming the foundation for model fine-tuning.  

### 🧮 Text Preprocessing Steps  
- **Extraction:** Retrieved text using `pdfplumber` (PDFs) and `python-docx` (Word docs).  
- **Segmentation:** Divided text into clause-level segments using linguistic cues.  
- **Cleaning:** Removed headers, numbering, and irrelevant metadata.  
- **Label Mapping:** Unified CUAD labels into a standardized taxonomy.  
- **Tier Assignment:** Allocated each label into Tiers 1–5 for review prioritization.  

---

## 🧠 Model Architecture  

### 1. Clause Classification  
- **Model:** Legal-BERT (fine-tuned)  
- **Objective:** Classify each clause into one of 41 legal categories and assign a Tier.  
- **Output:** `(Clause Text → Label → Tier)`  

### 2. Contract Summarization  
- **Model:** OpenAI GPT-4.1-mini  
- **Objective:** Generate abstractive summaries of entire contracts or tier-specific clauses.  
- **Output:** Professional, domain-aware summaries highlighting key legal implications.  

### 3. Integration  
The full pipeline integrates both modules to produce a **tiered summary** of each contract, combining structured classification with narrative summarization.  

---

## 🏷️ Tier System  

Clauses are organized into five **priority tiers** based on legal criticality and impact.  

| Tier | Description | Typical Clauses |
|------|--------------|----------------|
| **Tier 1 — Critical** | Core clauses that define fundamental obligations; require top-priority review. | Termination, Liability, IP Ownership, Governing Law, Exclusivity |
| **Tier 2 — Important** | Major operational and legal commitments. | Indemnification, Insurance, Non-Compete, Joint IP Ownership |
| **Tier 3 — Moderate** | Common operational clauses, standard across most contracts. | Renewal Terms, Warranty Duration |
| **Tier 4 — Low** | Administrative or low-impact clauses. | Notice Periods, Third-Party Beneficiary |
| **Tier 5 — Trivial / Informational** | Generic metadata and boilerplate. | Effective Date, Parties, Document Name |  

---

## 📊 Training & Evaluation  

### ⚙️ Setup  
- **Model:** Legal-BERT fine-tuned on `combined_clauses.csv`  
- **Hardware:** NVIDIA A100 / RTX-class GPU  
- **Metrics:** Accuracy, F1-Score, Training & Validation Loss  

### 📈 Results  

| Epoch | Training Loss | Validation Loss | Accuracy | F1 Score |
|--------|----------------|------------------|-----------|-----------|
| 1 | 0.9509 | 0.8081 | 0.7532 | 0.7043 |
| 2 | 0.6416 | 0.6663 | 0.7798 | 0.7432 |
| 3 | **0.5214** | **0.6565** | **0.7822** | **0.7549** |

**Final Training Summary:**  
```bash
TrainOutput(global_step=2913, training_loss=0.9271, metrics={
 'train_runtime': 25027.72,
 'train_samples_per_second': 0.931,
 'train_steps_per_second': 0.116,
 'total_flos': 3.07e15,
 'train_loss': 0.9271,
 'epoch': 3.0
})
```

✅ The model achieved strong generalization with an **Accuracy of 78.2%** and **F1 score of 75.5%**, demonstrating reliable clause identification and tier prediction across unseen contracts.  

---

## 📝 Output & Reporting  

**Generated Outputs:**  
- 📁 **CSV:**  
  `Clause | Predicted_Label | Tier`  
- 🎯 **Tier-wise Filtering:**  
  Extract or visualize specific tiers for focused review.  
- 🧾 **Summarization:**  
  Abstractive summaries using GPT-4.1-mini for each contract.  
- 📑 **PDF Reports:**  
  Visual tier distribution charts, clause summaries, and contract overviews.  

---

## 📈 Interpretation & Impact  

| Aspect | Impact |
|--------|---------|
| **Efficiency** | Automates repetitive clause review tasks, reducing manual effort. |
| **Prioritization** | Enables structured, tier-based clause assessment. |
| **Scalability** | Adaptable to various contract types and volumes. |
| **Practicality** | Seamless integration into legal dashboards or document review tools. |

Overall, the system achieves a **balanced trade-off between performance, interpretability, and automation**, making it a practical solution for legal contract intelligence.  

---

## 🔮 Future Directions  

- 🌍 Expansion to **multilingual contract datasets** and international law corpora.  
- 📚 Incorporation of **contextual retrieval** mechanisms using ACORD-style datasets.  
- 💻 Development of **interactive dashboards** for real-time clause visualization and review.  
- 🤝 Extension into **clause revision, negotiation support,** and legal reasoning tasks.  

---

✅ **In summary**, this project demonstrates a robust end-to-end Legal NLP pipeline integrating **Legal-BERT** and **GPT-4.1-mini** to automate clause classification, tier prioritization, and summarization — delivering measurable improvements in accuracy, interpretability, and review efficiency.  
