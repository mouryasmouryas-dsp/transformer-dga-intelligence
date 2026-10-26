
import pandas as pd

df = pd.read_excel(
    r"C:\Users\india\Downloads\FinalDataSet_DGA.xlsx"
)

print("Total records:", len(df))

print("\nFault categories:")
print(df["Fault"].value_counts(dropna=False))

# Keep only records with known fault labels
labelled_df = df.dropna(subset=["Fault"]).copy()

print("\nTotal labelled records:", len(labelled_df))

print("\nLabelled fault distribution:")
print(labelled_df["Fault"].value_counts())

# Check missing gas values in labelled records
gases = [
    "Hydrogen (H2)",
    "Methane (CH4)",
    "Ethylene (C2H4)",
    "Ethane (C2H6)",
    "Acetylene (C2H2)"
]

print("\nMissing values in labelled records:")
print(labelled_df[gases].isnull().sum())

print("\nLabelled samples:")
print(labelled_df[["Transformer", "Fault"]].to_string(index=False))
