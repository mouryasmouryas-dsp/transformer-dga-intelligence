
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. Load the dataset
df = pd.read_excel(
    r"C:\Users\india\OneDrive\Desktop\TRANSFORMER PROJECT\IEEE_STANDARD.xlsx"
)

# Rename the target column
df = df.rename(columns={"故障类型": "Fault Type"})

print("Original dataset shape:", df.shape)

# 2. Check duplicate records
print("\nDuplicate rows:", df.duplicated().sum())

# Remove exact duplicate rows for this initial experiment
df = df.drop_duplicates().reset_index(drop=True)

print("Shape after removing duplicates:", df.shape)

# 3. Separate input features (X) and target labels (y)
gases = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]

X = df[gases]
y = df["Fault Type"]

print("\nInput shape:", X.shape)
print("Target shape:", y.shape)

# 4. Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

print("\nTraining class distribution:")
print(y_train.value_counts())

print("\nTesting class distribution:")
print(y_test.value_counts())

# 5. Standardize the features
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\nScaled training shape:", X_train_scaled.shape)
print("Scaled testing shape:", X_test_scaled.shape)

print("\nPreprocessing completed successfully.")
