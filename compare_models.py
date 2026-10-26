
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# 1. Load dataset
df = pd.read_excel(
    r"C:\Users\india\OneDrive\Desktop\TRANSFORMER PROJECT\IEEE_STANDARD.xlsx"
)

df = df.rename(columns={"故障类型": "Fault Type"})
df = df.drop_duplicates().reset_index(drop=True)

gases = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]

X = df[gases]
y = df["Fault Type"]

# 2. Use the same train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# 3. Define the first three models
models = {
    "Gaussian Naive Bayes": make_pipeline(
        StandardScaler(),
        GaussianNB()
    ),

    "Logistic Regression": make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=3000, random_state=42)
    ),

    "Initial SVM": make_pipeline(
        StandardScaler(),
        SVC(kernel="rbf", C=1.0, gamma="scale")
    )
}

# 4. Cross-validation setup
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

# 5. Tune SVM using training data only
svm_search = GridSearchCV(
    make_pipeline(StandardScaler(), SVC()),
    {
        "svc__kernel": ["rbf"],
        "svc__C": [0.1, 1, 10, 100],
        "svc__gamma": ["scale", 0.01, 0.1, 1]
    },
    scoring="f1_macro",
    cv=cv,
    n_jobs=-1
)

svm_search.fit(X_train, y_train)
models["Tuned SVM"] = svm_search.best_estimator_

# 6. Tune Random Forest using training data only
rf_search = GridSearchCV(
    RandomForestClassifier(
        random_state=42,
        class_weight="balanced"
    ),
    {
        "n_estimators": [100, 200],
        "max_depth": [None, 10, 20],
        "min_samples_leaf": [1, 2, 4]
    },
    scoring="f1_macro",
    cv=cv,
    n_jobs=-1
)

rf_search.fit(X_train, y_train)
models["Random Forest"] = rf_search.best_estimator_

# 7. Evaluate every model on the same test set
results = []

for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, predictions),
        "Macro Precision": precision_score(
            y_test, predictions, average="macro", zero_division=0
        ),
        "Macro Recall": recall_score(
            y_test, predictions, average="macro", zero_division=0
        ),
        "Macro F1": f1_score(
            y_test, predictions, average="macro", zero_division=0
        )
    })

# 8. Display results
results_df = pd.DataFrame(results)

print("\nFINAL MODEL COMPARISON")
print("======================")
print(results_df.round(4).to_string(index=False))

print("\nBest SVM parameters:")
print(svm_search.best_params_)
print("SVM CV macro F1:", round(svm_search.best_score_, 4))

print("\nBest Random Forest parameters:")
print(rf_search.best_params_)
print("Random Forest CV macro F1:", round(rf_search.best_score_, 4))
