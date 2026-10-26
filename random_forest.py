
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score
)

# 1. Load dataset
df = pd.read_excel(
    r"C:\Users\india\OneDrive\Desktop\TRANSFORMER PROJECT\IEEE_STANDARD.xlsx"
)

# 2. Rename target column and remove exact duplicates
df = df.rename(columns={"故障类型": "Fault Type"})
df = df.drop_duplicates().reset_index(drop=True)

# 3. Select gas features and target
gases = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]

X = df[gases]
y = df["Fault Type"]

# 4. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# 5. Create Random Forest model
model = RandomForestClassifier(
    random_state=42,
    class_weight="balanced"
)

# 6. Define parameters to test
param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [None, 10, 20],
    "min_samples_leaf": [1, 2, 4]
}

# 7. Set up cross-validation
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

# 8. Tune using training data only
search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    scoring="f1_macro",
    cv=cv,
    n_jobs=-1
)

search.fit(X_train, y_train)

# 9. Evaluate best model on test data
best_model = search.best_estimator_
y_pred = best_model.predict(X_test)

print("Random Forest Results")
print("----------------------")
print("Best parameters:", search.best_params_)
print("Best CV macro F1:", round(search.best_score_, 4))
print("Test accuracy:", round(accuracy_score(y_test, y_pred), 4))
print("Test macro F1:", round(f1_score(
    y_test, y_pred, average="macro", zero_division=0
), 4))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred, labels=best_model.classes_))

print("\nClass order:", best_model.classes_)
