
import pandas as pd

# 1. Model comparison results
models = pd.DataFrame({
    "Model": [
        "Gaussian Naive Bayes",
        "Logistic Regression",
        "Initial SVM",
        "Tuned SVM",
        "Random Forest"
    ],
    "Accuracy (%)": [
        41.53, 48.31, 28.81, 64.41, 75.42
    ],
    "Macro F1": [
        0.3293, 0.3284, 0.1270, 0.5544, 0.7382
    ]
})

# 2. Grouped cross-validation results
validation = pd.DataFrame({
    "Metric": [
        "Mean accuracy",
        "Accuracy standard deviation",
        "Mean macro F1",
        "Macro F1 standard deviation"
    ],
    "Value": [
        0.7751, 0.0151, 0.7678, 0.0156
    ]
})

# 3. Permutation importance
importance = pd.DataFrame({
    "Gas": ["C2H4", "C2H2", "H2", "C2H6", "CH4"],
    "Mean importance": [0.3534, 0.3202, 0.1865, 0.1225, 0.0504],
    "Fold standard deviation": [
        0.0128, 0.0208, 0.0381, 0.0188, 0.0287
    ]
})

# 4. Print tables
print("MODEL COMPARISON")
print("================")
print(models.to_string(index=False))

print("\nGROUPED CROSS-VALIDATION")
print("=======================")
print(validation.to_string(index=False))

print("\nPERMUTATION FEATURE IMPORTANCE")
print("==============================")
print(importance.to_string(index=False))

# 5. Save tables for the report
models.to_csv("model_comparison.csv", index=False)
validation.to_csv("grouped_validation_summary.csv", index=False)
importance.to_csv("permutation_importance_summary.csv", index=False)

print("\nSaved:")
print("model_comparison.csv")
print("grouped_validation_summary.csv")
print("permutation_importance_summary.csv")
