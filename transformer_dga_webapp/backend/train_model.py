"""
Train and save the Random Forest model artifact.

This script reproduces the exact training procedure from the original project:
1. Load IEEE_STANDARD.xlsx
2. Rename 故障类型 → Fault Type
3. Drop exact duplicate rows
4. Use features ["H2", "CH4", "C2H6", "C2H4", "C2H2"]
5. Train/test split: 80/20, random_state=42, stratify=y
6. GridSearchCV with the original parameter grid
7. Save the best estimator and metadata

The Random Forest is trained on raw ppm values (no StandardScaler),
matching the original random_forest.py script.
"""

import json
import os
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split

# ─── Paths ───────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_DIR = os.path.dirname(APP_DIR)

DATASET_PATH = os.path.join(PROJECT_DIR, "IEEE_STANDARD.xlsx")
MODEL_DIR = os.path.join(APP_DIR, "models")
CONFIG_DIR = os.path.join(APP_DIR, "config")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)


def train_and_save():
    """Train the Random Forest following the original project procedure."""

    # 1. Load dataset
    print("Loading dataset:", DATASET_PATH)
    df = pd.read_excel(DATASET_PATH)
    df = df.rename(columns={"故障类型": "Fault Type"})
    df = df.drop_duplicates().reset_index(drop=True)

    print(f"Dataset shape after dedup: {df.shape}")

    # 2. Separate features and target
    gases = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]
    X = df[gases]
    y = df["Fault Type"]

    print(f"\nClass distribution:\n{y.value_counts()}")

    # 3. Train/test split (identical to original)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f"\nTraining samples: {len(X_train)}")
    print(f"Testing samples:  {len(X_test)}")

    # 4. Grid search (identical to original random_forest.py)
    model = RandomForestClassifier(random_state=42, class_weight="balanced")

    param_grid = {
        "n_estimators": [100, 200],
        "max_depth": [None, 10, 20],
        "min_samples_leaf": [1, 2, 4],
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring="f1_macro",
        cv=cv,
        n_jobs=-1,
    )

    print("\nRunning grid search...")
    search.fit(X_train, y_train)

    best_model = search.best_estimator_
    y_pred = best_model.predict(X_test)

    # 5. Evaluate
    test_accuracy = accuracy_score(y_test, y_pred)
    test_f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)

    print(f"\nBest parameters: {search.best_params_}")
    print(f"Best CV macro F1: {search.best_score_:.4f}")
    print(f"Test accuracy:    {test_accuracy:.4f}")
    print(f"Test macro F1:    {test_f1:.4f}")

    print("\nClassification Report:")
    report = classification_report(y_test, y_pred, zero_division=0, output_dict=True)
    print(classification_report(y_test, y_pred, zero_division=0))

    print("Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred, labels=sorted(y.unique()))
    print(cm)
    print(f"\nClass order: {sorted(y.unique())}")

    # 6. Save model
    model_path = os.path.join(MODEL_DIR, "random_forest_model.joblib")
    joblib.dump(best_model, model_path)
    print(f"\nModel saved: {model_path}")

    # 7. Compute training data statistics for OOD detection
    train_stats = {}
    for gas in gases:
        train_stats[gas] = {
            "min": float(X_train[gas].min()),
            "max": float(X_train[gas].max()),
            "mean": float(X_train[gas].mean()),
            "std": float(X_train[gas].std()),
            "q25": float(X_train[gas].quantile(0.25)),
            "q75": float(X_train[gas].quantile(0.75)),
        }

    # Full dataset stats for visualization
    full_stats = {}
    for gas in gases:
        full_stats[gas] = {
            "min": float(X[gas].min()),
            "max": float(X[gas].max()),
            "mean": float(X[gas].mean()),
            "std": float(X[gas].std()),
            "q25": float(X[gas].quantile(0.25)),
            "q75": float(X[gas].quantile(0.75)),
        }

    # 8. Save metadata
    metadata = {
        "model_version": "1.0.0",
        "algorithm": "RandomForestClassifier",
        "best_params": search.best_params_,
        "feature_names": gases,
        "class_labels": sorted(y.unique().tolist()),
        "training_unit": "ppm",
        "preprocessing": "none",
        "dataset": {
            "filename": "IEEE_STANDARD.xlsx",
            "total_rows_raw": 589,
            "total_rows_deduped": len(df),
            "train_samples": len(X_train),
            "test_samples": len(X_test),
        },
        "holdout_metrics": {
            "accuracy": round(test_accuracy, 4),
            "macro_f1": round(test_f1, 4),
            "classification_report": report,
        },
        "confusion_matrix": cm.tolist(),
        "confusion_matrix_labels": sorted(y.unique().tolist()),
        "train_data_stats": train_stats,
        "full_data_stats": full_stats,
    }

    metadata_path = os.path.join(CONFIG_DIR, "model_metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2, default=str)
    print(f"Metadata saved: {metadata_path}")

    # 9. Verify the saved model produces identical predictions
    loaded_model = joblib.load(model_path)
    y_verify = loaded_model.predict(X_test)
    assert np.array_equal(y_pred, y_verify), "Model verification FAILED!"
    print("\n✓ Model verification passed: saved model reproduces identical predictions.")

    return best_model, metadata


if __name__ == "__main__":
    train_and_save()
