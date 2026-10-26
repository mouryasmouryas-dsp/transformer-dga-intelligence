
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_excel(
    r"C:\Users\india\OneDrive\Desktop\TRANSFORMER PROJECT\IEEE_STANDARD.xlsx"
)

# Rename the target column
df = df.rename(columns={"故障类型": "Fault Type"})

# Select gas features
gases = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]

# 1. Basic dataset information
print("Dataset shape:", df.shape)
print("\nData types:")
print(df.dtypes)

print("\nFault class counts:")
print(df["Fault Type"].value_counts())

print("\nDuplicate rows:", df.duplicated().sum())

# 2. Plot fault class distribution
df["Fault Type"].value_counts().plot(
    kind="bar",
    rot=0
)
plt.title("Transformer Fault Class Distribution")
plt.xlabel("Fault Type")
plt.ylabel("Number of Samples")
plt.tight_layout()
plt.show()

# 3. Plot gas distributions
df[gases].hist(figsize=(10, 7), bins=25)
plt.suptitle("Distribution of Dissolved Gas Concentrations")
plt.tight_layout()
plt.show()

# 4. Plot gas correlation heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(
    df[gases].corr(),
    annot=True,
    fmt=".2f",
    cmap="coolwarm"
)
plt.title("Correlation Between Gas Features")
plt.tight_layout()
plt.show()

# 5. Compare gas measurements across fault classes
for gas in gases:
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x="Fault Type", y=gas)
    plt.title(gas + " Concentration Across Fault Classes")
    plt.tight_layout()
    plt.show()
