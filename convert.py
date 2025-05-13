import pandas as pd

# === Input and Output Files ===
input_xlsx = 'source files/en-zh_claude.xlsx'   # Replace with your actual file name
output_csv = 'source files/En_Zh_claude.csv'

# === Read Excel File ===
df = pd.read_excel(input_xlsx)

# === Add Index Column ===
df.reset_index(inplace=True)
df.rename(columns={'index': 'Index'}, inplace=True)

# === Save as CSV ===
df.to_csv(output_csv, index=False)

print(f"Conversion complete. Saved as {output_csv}")
