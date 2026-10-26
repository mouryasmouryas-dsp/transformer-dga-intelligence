
import pandas as pd

file_path = r"C:\Users\india\OneDrive\Desktop\TRANSFORMER PROJECT\IEEE_STANDARD.xlsx"

df = pd.read_excel(file_path)
df = df.rename(columns={"故障类型": "Fault Type"})

gases = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]

# Find all rows sharing the same five gas readings
conflicts = df[
    df.duplicated(subset=gases, keep=False)
].sort_values(gases + ["Fault Type"])

print("Total rows with repeated gas readings:", len(conflicts))

print("\nAll repeated readings and their labels:")
print(conflicts.to_string(index=False))

# Count distinct labels for each repeated reading
summary = (
    conflicts.groupby(gases, dropna=False)
    .agg(
        Number_of_rows=("Fault Type", "size"),
        Number_of_labels=("Fault Type", "nunique"),
        Labels=("Fault Type", lambda s: ", ".join(sorted(set(s))))
    )
    .reset_index()
)

print("\nSummary of repeated readings:")
print(summary.to_string(index=False))

print("\nRepeated readings with conflicting labels:")
print(summary[summary["Number_of_labels"] > 1].to_string(index=False))
