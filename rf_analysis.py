
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import StratifiedGroupKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

# 1. Load and prepare the dataset
path = r"C:\Users\india\OneDrive\Desktop\TRANSFORMER PROJECT\IEEE_STANDARD.xlsx"

df = pd.read_excel(path)
df = df.rename(columns={"故障类型": "Fault Type"})
df = df.drop_duplicates().reset_index(drop=True)

gases = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]

X = df[gases]
y = df["Fault Type"]

# 2. Group identical gas readings together
groups = pd.factorize(pd.MultiIndex.from_frame(X))[0]

# 3. Define the model and cross-validation
cv = StratifiedGroupKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42
)

# 4. Evaluate each fold separately
fold_results = []

for fold, (train_idx, test_idx) in enumerate(
    cv.split(X, y, groups), start=1
):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    macro_f1 = f1_score(
        y_test, predictions, average="macro", zero_division=0
    )

    fold_results.append({
        "Fold": fold,
        "Test samples": len(test_idx),
        "Accuracy": accuracy,
        "Macro F1": macro_f1
    })

results = pd.DataFrame(fold_results)

print("FOLD-BY-FOLD RESULTS")
print("====================")
print(results.round(4).to_string(index=False))

print("\nMean accuracy:", round(results["Accuracy"].mean(), 4))
print("Accuracy standard deviation:", round(results["Accuracy"].std(), 4))
print("Mean macro F1:", round(results["Macro F1"].mean(), 4))
print("Macro F1 standard deviation:", round(results["Macro F1"].std(), 4))

# 5. Fit on the full dataset for exploratory feature importance
model.fit(X, y)

importance = pd.DataFrame({
    "Gas": gases,
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=False)

print("\nFEATURE IMPORTANCE")
print("==================")
print(importance.round(4).to_string(index=False))

# 6. Plot fold accuracy
plt.figure(figsize=(7, 4))
plt.bar(results["Fold"].astype(str), results["Accuracy"])
plt.xlabel("Cross-validation fold")
plt.ylabel("Accuracy")
plt.title("Random Forest: Accuracy by Fold")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig("rf_fold_accuracy.png", dpi=300)
plt.show()

# 7. Plot feature importance
plt.figure(figsize=(7, 4))
plt.bar(importance["Gas"], importance["Importance"])
plt.xlabel("Dissolved gas")
plt.ylabel("Feature importance")
plt.title("Random Forest: Gas Feature Importance")
plt.tight_layout()
plt.savefig("rf_feature_importance.png", dpi=300)
plt.show()

print("\nSaved plots:")
print("rf_fold_accuracy.png")
print("rf_feature_importance.png")
