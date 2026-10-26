
import pandas as pd
import numpy as np

# 1. Load dataset
file_path = r"C:\Users\india\OneDrive\Desktop\TRANSFORMER PROJECT\IEEE_STANDARD.xlsx"

df = pd.read_excel(file_path)
df = df.rename(columns={"故障类型": "Fault Type"})

gases = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]

print("DATASET VALIDATION")
print("==================")

# 2. Dataset size and columns
print("\nDataset shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

# 3. Missing values
print("\nMissing values:")
print(df.isnull().sum())

# 4. Duplicate rows
print("\nExact duplicate rows:", df.duplicated().sum())

# 5. Check data types
print("\nData types:")
print(df.dtypes)

# 6. Check gas values
print("\nGas concentration summary:")
print(df[gases].describe().round(3))

# 7. Check invalid gas concentrations
print("\nNegative gas concentrations:")
print((df[gases] < 0).sum())

print("\nInfinite gas values:")
print(
    pd.DataFrame(
        np.isinf(df[gases].to_numpy()),
        columns=gases
    ).sum()
)

# 8. Check fault class counts
print("\nFault class counts:")
print(df["Fault Type"].value_counts(dropna=False))

# 9. Check whether duplicate gas readings have conflicting labels
duplicate_gases = df[
    df.duplicated(subset=gases, keep=False)
].sort_values(gases)

print("\nRows sharing identical gas readings:", len(duplicate_gases))

if len(duplicate_gases) > 0:
    print("\nLabels for identical gas readings:")
    print(
        duplicate_gases.groupby(gases, dropna=False)["Fault Type"]
        .agg(["count", "nunique"])
        .sort_values("nunique", ascending=False)
        .head(10)
    )

print("\nValidation checks completed.")
