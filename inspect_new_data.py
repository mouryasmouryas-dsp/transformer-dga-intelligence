
import pandas as pd

df = pd.read_excel(
    r"C:\Users\india\OneDrive\Desktop\TRANSFORMER PROJECT\IEEE_STANDARD.xlsx"
)

# Replace Chinese column name with English
df = df.rename(columns={"故障类型": "Fault Type"})

print("Dataset shape:", df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst five rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nFault distribution:")
print(df["Fault Type"].value_counts(dropna=False))
