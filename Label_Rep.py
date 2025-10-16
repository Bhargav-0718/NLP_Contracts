import os
import pandas as pd

# Path to your folder containing the 28 Excel files
folder_path = "D:\\AI\\Projects\\Contract_NLP\\CUAD_v1\\label_group_xlsx"
output_csv = "combined_clauses.csv"

# List to collect all DataFrames
all_data = []

# Loop through each Excel file in the folder
for file in os.listdir(folder_path):
    if file.endswith(".xlsx") or file.endswith(".xls"):
        file_path = os.path.join(folder_path, file)

        # Read Excel
        df = pd.read_excel(file_path)

        # Drop Filename column (case-insensitive match just in case)
        df = df.loc[:, ~df.columns.str.contains("filename", case=False)]

        # Reshape: melt into Clause + Label
        df_melted = df.melt(var_name="Label", value_name="Clause")

        # Drop empty rows
        df_melted = df_melted.dropna(subset=["Clause"])

        all_data.append(df_melted)

# Combine all into one DataFrame
combined_df = pd.concat(all_data, ignore_index=True)

# Save to CSV
combined_df.to_csv(output_csv, index=False)

print(f"✅ Combined CSV saved to: {output_csv}")
