
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import StratifiedGroupKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import f1_score

# 1. Load and prepare data
path = r"C:\Users\india\OneDrive\Desktop\TRANSFORMER PROJECT\IEEE_STANDARD.xlsx"

df = pd.read_excel(path)
df = df.rename(columns={"故障类型": "Fault Type"})
df = df.drop_duplicates().reset_index(drop=True)

gases = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]
X = df[gases]
y = df["Fault Type"]

# 2. Group identical gas readings together
groups = pd.factorize(pd.MultiIndex.from_frame(X))[0]

# 3. Set up grouped cross-validation
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

# 4. Calculate permutation importance on each held-out fold
fold_importances = []

for fold, (train_idx, test_idx) in enumerate(
    cv.split(X, y, groups), start=1
):
    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]
    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]

    model.fit(X_train, y_train)

    result = permutation_importance(
        model,
        X_test,
        y_test,
        scoring="f1_macro",
        n_repeats=20,
        random_state=42,
        n_jobs=-1
    )

    for i, gas in enumerate(gases):
        fold_importances.append({
            "Fold": fold,
            "Gas": gas,
            "Importance": result.importances_mean[i],
            "Std": result.importances_std[i]
        })

# 5. Summarize importance across folds
importance_df = pd.DataFrame(fold_importances)

summary = (
    importance_df.groupby("Gas")
    .agg(
        Mean_Importance=("Importance", "mean"),
        Fold_Std=("Importance", "std")
    )
    .sort_values("Mean_Importance", ascending=False)
)

print("PERMUTATION IMPORTANCE")
print("======================")
print(summary.round(4).to_string())

# 6. Plot the results
plot_data = summary.sort_values("Mean_Importance")

plt.figure(figsize=(8, 5))
plt.barh(
    plot_data.index,
    plot_data["Mean_Importance"],
    xerr=plot_data["Fold_Std"]
)
plt.axvline(0, linewidth=1)
plt.xlabel("Decrease in macro F1 after shuffling")
plt.ylabel("Gas feature")
plt.title("Grouped-CV Permutation Importance")
plt.tight_layout()
plt.savefig("permutation_importance.png", dpi=300)
plt.show()

print("\nSaved plot: permutation_importance.png")
