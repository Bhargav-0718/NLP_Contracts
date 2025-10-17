# 📜 NLP Contract Summarization & Risk-Sensitive Clause Review

This project explores **NLP-based approaches** for **contract summarization** and **risk-sensitive clause review**, leveraging transformer-based models to help lawyers and organizations efficiently analyze complex contracts.

---

## 🚀 Problem Statement

Contracts often contain **thousands of clauses** with varying risk levels. Manual review is time-consuming and error-prone. This project aims to:

* Extract **key obligations, risks, and liabilities** from contracts.
* Generate **abstractive summaries** for faster contract understanding.
* Flag and suggest **revisions** for risky clauses.
* **Tier clauses by criticality** to guide legal expert review.
* Provide **graphical insights** for contract analysis (pie charts, bar charts, and more).

---

## 📚 Literature Review

We studied several datasets and benchmarks for legal NLP tasks:

* **CUAD (Contract Understanding Atticus Dataset)** → Clause-span extraction with ~13K expert annotations.
* **MAUD (Merger Agreement Understanding Dataset)** → Question-answering on merger agreements.
* **LexGLUE / LEDGAR** → Large-scale provision classification from SEC filings.
* **LegalBench** → Benchmark for legal reasoning tasks.
* **ACORD** → Clause retrieval dataset for drafting workflows.
* **Other works** explored party-specific summarization, abstractive summarization of obligations, and smart contract summarization.

📖 References:

* [CUAD Paper](https://arxiv.org/abs/2103.06268) | [CUAD GitHub](https://github.com/TheAtticusProject/cuad)
* [MAUD](https://arxiv.org/html/2301.00876)
* [LexGLUE](https://aclanthology.org/2022.acl-long.297.pdf)
* [LegalBench](https://arxiv.org/abs/2308.11462)

---

## 📂 Dataset

We primarily used **CUAD**, consisting of:

* **510 commercial contracts**.
* **13K expert-annotated clauses** across **41 clause types** (e.g., *Termination, Liability, Indemnification*).
* Preprocessed into a **2-column dataset**: `[clause, label]`.
* Labels mapped to **5 Tiers** for risk-prioritization in legal review.

---

## ⚙️ Preprocessing

* **PDF/DOCX extraction** using `pdfplumber` and `python-docx`.
* **Segmentation** into clauses/paragraphs.
* **Cleaning**: removal of headers/footers, whitespace normalization.
* **Clause Classification**: map clause text → contract clause type → numeric label → Tier.

---

## 🧠 Model Architecture

* **Base Model**: [Legal-BERT](https://huggingface.co/nlpaueb/legal-bert-base-uncased).
* **Clause Classification**: maps clause text → clause label → Tier.
* **Summarization**: abstractive models (BART/PEGASUS fine-tuned or Gen AI) for generating contract summaries.
* **Risk-Sensitive Revision**: generative LLM prompts suggest safer clause rewrites.

---

## 🔢 Tier System for Clauses

Clauses are grouped into **5 Tiers** based on **criticality**:

| Tier                   | Labels / Clauses (CUAD)                                                                                                                                                                                                                                                                                                                                                                                                          | Notes                                                                          |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| 1 (Critical)           | Anti-assignment, Audit Rights, Cap on Liability, Exclusivity, Governing Law, IP Ownership Assignment, Liquidated Damages, Non-Compete, Termination for Convenience, Uncapped Liability                                                                                                                                                                                                                                           | Clauses that **must be reviewed** by legal experts. High-risk or high-impact.  |
| 2 (Important)          | Competitive Restriction Exception, Covenant not to Sue, Insurance, Irrevocable or Perpetual License, Joint IP Ownership, License Grant, Minimum Commitment, Most Favored Nation, No-Solicit of Customers, No-Solicit of Employees, Non-Disparagement, Non-Transferable License, Post-termination Services, Price Restrictions, Revenue-Profit Sharing, Source Code Escrow, Unlimited/All-You-Can-Eat License, Volume Restriction | Important clauses, usually reviewed. Moderate risk or contractual obligations. |
| 3 (Moderate)           | Change of Control, Renewal Term, Renewal Term-Answer, Warranty Duration                                                                                                                                                                                                                                                                                                                                                          | Standard or moderate-risk clauses. Less critical than Tier 1 & 2.              |
| 4 (Low)                | Notice Period to Terminate Renewal, Notice Period to Terminate Renewal-Answer, ROFR-ROFO-ROFN, Third Party Beneficiary                                                                                                                                                                                                                                                                                                           | Low criticality. Often procedural or informational.                            |
| 5 (Trivial / Optional) | Affiliate License-Licensee, Affiliate License-Licensor, Agreement Date, Agreement Date-Answer, Document Name, Effective Date, Effective Date-Answer, Expiration Date, Expiration Date-Answer, Parties, Parties-Answer                                                                                                                                                                                                            | Minimal review needed. Administrative or non-substantive clauses.              |

**Explanation:**

* **Tier 1** → High-priority clauses that **require legal expert review**.
* **Tier 2** → Important clauses, usually reviewed but lower risk than Tier 1.
* **Tier 3** → Moderate risk, standard clauses.
* **Tier 4** → Low-risk clauses; procedural or informative.
* **Tier 5** → Trivial clauses; may be skipped in automated review (e.g., names, dates, document info).

---

## 📊 Training & Evaluation

* Fine-tuned **Legal-BERT** on CUAD clause-label dataset.
* Metrics: **Accuracy, F1 Score**.
* Results:

  * Automatic clause classification reduces manual review time.
  * Legal-BERT effectively classifies complex clauses.
  * Tier system guides legal experts to focus on **high-risk clauses**.
  * Risk-sensitive revisions provide actionable insights for lawyers.

---

## 📝 Output & Reporting

* **Classified CSV** with:
  `predicted_class_id` | `Predicted Label` | `Tier` | `Clause`
* **Tiered reporting** allows filtering:
  * Focus on **Tier 1–2** clauses for legal review.
  * **Tier 3–5** for reference or optional inspection.
* **Abstractive summaries** generated using Gen AI summarize the contract at a high level.
* **Comprehensive PDF Reports** include:
  * Formatted **contract summary** with headings, bold key points.
  * Visual **graphs** (pie charts, bar charts) for clause distribution, tier analysis, top clauses by frequency.
  * Professional layout in **Times New Roman**, suitable for stakeholder presentation.

---

## 📈 Visual Insights in the Report

* **Pie charts**: distribution of clauses by Tier.
* **Bar charts**: number of clauses per label, top 5 risky clauses.
* **Combined graphs**: multi-view dashboard for contract analysis.
* Graphs saved in a **Graphs/** folder and embedded in the PDF report.

---

## 🔮 Interpretation & Impact

* **Efficiency**: Faster contract review process with prioritized clauses.
* **Risk Management**: Highlights clauses that may expose organizations to liability.
* **Comprehensive Analysis**: Summary + visual analytics give stakeholders a complete view.
* **Practical Use**: Can be integrated into **contract management systems**, legal AI assistants, or internal compliance dashboards.

---

## ⚡ Next Steps / Extensions

* Integrate **automated alerts** for high-risk clause changes.
* Add **multi-contract comparison** dashboards.
* Extend to **multi-language contract processing**.
* Add **interactive PDF reports** with clickable TOC and embedded charts.

---

