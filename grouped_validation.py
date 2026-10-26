
import pandas as pd

from sklearn.model_selection import StratifiedGroupKFold, cross_val_predict
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score
)

# 1. Load data
path = r"C:\Users\india\OneDrive\Desktop\TRANSFORMER PROJECT\IEEE_STANDARD.xlsx"

df = pd.read_excel(path)
df = df.rename(columns={"故障类型": "Fault Type"})
df = df.drop_duplicates().reset_index(drop=True)

gases = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]

X = df[gases]
y = df["Fault Type"]

# 2. Give identical gas readings the same group ID
groups = pd.factorize(
    pd.MultiIndex.from_frame(X)
)[0]

print("Rows after exact duplicate removal:", len(df))
print("Unique gas-reading groups:", len(set(groups)))
print("Repeated-reading groups:", len(df) - len(set(groups)))

# 3. Grouped, stratified five-fold cross-validation
cv = StratifiedGroupKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

# 4. Use the previously selected Random Forest settings
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42
)

# Each prediction is made when its entire gas-reading group
# is excluded from the corresponding training fold.
predictions = cross_val_predict(
    model,
    X,
    y,
    cv=cv,
    groups=groups
)

# 5. Evaluate all out-of-fold predictions
print("\nGROUPED VALIDATION RESULTS")
print("==========================")
print("Accuracy:", round(accuracy_score(y, predictions), 4))
print(
    "Macro F1:",
    round(f1_score(y, predictions, average="macro"), 4)
)

print("\nClassification Report:")
print(classification_report(y, predictions, zero_division=0))

print("\nConfusion Matrix:")
print(confusion_matrix(y, predictions, labels=sorted(y.unique())))

print("\nClass order:", sorted(y.unique()))
