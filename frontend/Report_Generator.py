
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

csv_path = ("D:\AI\Projects\Contract_NLP\output\classified_contract.csv")
summary_path =("D:\AI\Projects\Contract_NLP\output\Contract_Abstractive_Summary.txt")
graphs_dir = ("D:\AI\Projects\Contract_NLP\Graphs")
output_pdf = ("D:\AI\Projects\Contract_NLP\Contract_Analysis_Report.pdf")

os.makedirs(graphs_dir, exist_ok=True)

def generate_graphs(df, graphs_dir):
    # Tier Distribution
    tier_counts = df['Tier'].value_counts().sort_index()
    plt.figure(figsize=(6,6))
    colors = sns.color_palette("RdYlGn_r", len(tier_counts))
    plt.pie(tier_counts, labels=[f"Tier {i}" for i in tier_counts.index], autopct='%1.1f%%', colors=colors)
    plt.title("Clause Distribution by Tier")
    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, "tier_distribution.png"))
    plt.close()


    # Label Frequency
    label_counts = df['Predicted Label'].value_counts()
    plt.figure(figsize=(10,6))
    sns.barplot(x=label_counts.values, y=label_counts.index, palette="viridis")
    plt.xlabel("Number of Clauses")
    plt.ylabel("Clause Label")
    plt.title("Number of Clauses per Label")
    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, "label_frequency.png"))
    plt.show()

    # Heatmap Tier vs Label
    tier_label_matrix = pd.crosstab(df['Predicted Label'], df['Tier'])
    plt.figure(figsize=(12,10))
    sns.heatmap(tier_label_matrix, annot=True, fmt="d", cmap="YlGnBu")
    plt.title("Clause Labels vs Tier Heatmap")
    plt.savefig(os.path.join(graphs_dir, "tier_label_heatmap.png"))
    plt.close()

    # Clause Length Distribution
    df['Clause_Length'] = df['Clause'].apply(lambda x: len(x.split()))
    plt.figure(figsize=(8,5))
    sns.histplot(df['Clause_Length'], bins=20, kde=True, color="skyblue")
    plt.xlabel("Number of Words")
    plt.ylabel("Frequency")
    plt.title("Distribution of Clause Lengths")
    plt.savefig(os.path.join(graphs_dir, "clause_length_distribution.png"))
    plt.close()

    # Expert Review vs Low Risk
    df['Review_Need'] = df['Tier'].apply(lambda x: 'Requires Review' if x <=2 else 'Low Risk')
    review_counts = df['Review_Need'].value_counts()
    plt.figure(figsize=(6,6))
    colors = ["#FF4C4C", "#4CAF50"]
    plt.pie(review_counts, labels=review_counts.index, autopct='%1.1f%%', colors=colors)
    plt.title("Clauses Requiring Expert Review vs Low Risk")
    plt.savefig(os.path.join(graphs_dir, "review_vs_lowrisk.png"))
    plt.close()

def generate_pdf_report(csv_path, summary_path, output_pdf, graphs_dir):
    import pandas as pd
    import os
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch

    # Read CSV and summary
    df = pd.read_csv(csv_path)
    with open(summary_path, "r", encoding="utf-8") as f:
        summary_text = f.read()

    # Generate graphs
    generate_graphs(df, graphs_dir)

    doc = SimpleDocTemplate(output_pdf, pagesize=A4,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='MyHeading1',
                          fontName='Times-Bold',
                          fontSize=16,
                          spaceAfter=14))
    styles.add(ParagraphStyle(name='MyHeading2',
                          fontName='Times-Bold',
                          fontSize=14,
                          spaceAfter=10))
    styles.add(ParagraphStyle(name='MyBodyText',
                          fontName='Times-Roman',
                          fontSize=12,
                          leading=18,
                          spaceAfter=8))
    styles.add(ParagraphStyle(name='MyBullet',
                          fontName='Times-Roman',
                          fontSize=12,
                          leading=16,
                          leftIndent=20,
                          spaceAfter=4))

    elements = []
    elements.append(Paragraph("Comprehensive Contract Analysis Report", styles['Heading1']))
    elements.append(Spacer(1,12))

    lines = summary_text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("**") or ":" in line:
            line = line.replace("**", "") 
            elements.append(Paragraph(line, styles['Heading2']))
        elif line.startswith("-"):
            line = line.lstrip("- ").strip()
            elements.append(Paragraph("• " + line, styles['Bullet']))
        else:
            elements.append(Paragraph(line, styles['BodyText']))
    elements.append(Spacer(1,12))
    

    # Add graphs
    graph_files = [
        ("tier_distribution.png", "Clause Distribution by Tier"),
        ("label_frequency.png", "Number of Clauses per Label"),
        ("tier_label_heatmap.png", "Clause Labels vs Tier Heatmap"),
        ("clause_length_distribution.png", "Distribution of Clause Lengths"),
        ("review_vs_lowrisk.png", "Clauses Requiring Expert Review vs Low Risk")
    ]
    for gf, title in graph_files:
        elements.append(Paragraph(title, styles['MyHeading2']))
        elements.append(Spacer(1,6))
        img_path = os.path.join(graphs_dir, gf)
        if os.path.exists(img_path):
            img = Image(img_path, width=6.5*inch, height=4*inch)
            elements.append(img)
            elements.append(Spacer(1,12))

    doc.build(elements)
    print(f"✅ PDF report generated: {output_pdf}")
