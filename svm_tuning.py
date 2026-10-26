
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# 1. Load dataset
df = pd.read_excel(
    r"C:\Users\india\OneDrive\Desktop\TRANSFORMER PROJECT\IEEE_STANDARD.xlsx"
)

# 2. Rename target column and remove exact duplicates
df = df.rename(columns={"故障类型": "Fault Type"})
df = df.drop_duplicates().reset_index(drop=True)

# 3. Separate gas features and fault labels
gases = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]

X = df[gases]
y = df["Fault Type"]

# 4. Create the same train-test split as previous models
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# 5. Build a pipeline
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC())
])

# 6. Define hyperparameters to test
param_grid = {
    "svm__kernel": ["rbf"],
    "svm__C": [0.1, 1, 10, 100],
    "svm__gamma": ["scale", 0.01, 0.1, 1]
}

# 7. Five-fold stratified cross-validation
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

# 8. Search for the best settings using macro F1
search = GridSearchCV(
    estimator=pipeline,
    param_grid=param_grid,
    scoring="f1_macro",
    cv=cv,
    n_jobs=-1,
    refit=True
)

search.fit(X_train, y_train)

# 9. Evaluate the selected model on the test set
best_model = search.best_estimator_
y_pred = best_model.predict(X_test)

print("Tuned SVM Results")
print("-----------------")
print("Best parameters:", search.best_params_)
print("Best cross-validation macro F1:", round(search.best_score_, 4))
print("Test accuracy:", round(accuracy_score(y_test, y_pred), 4))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred, labels=best_model.classes_))

print("\nClass order:", best_model.classes_)
