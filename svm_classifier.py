
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
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

# 2. Rename target column
df = df.rename(columns={"故障类型": "Fault Type"})

# 3. Remove exact duplicate rows
df = df.drop_duplicates().reset_index(drop=True)

# 4. Select gas features and target
gases = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]

X = df[gases]
y = df["Fault Type"]

# 5. Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# 6. Create SVM model
model = make_pipeline(
    StandardScaler(),
    SVC(kernel="rbf", C=1.0, gamma="scale")
)

# 7. Train the model
model.fit(X_train, y_train)

# 8. Predict fault types
y_pred = model.predict(X_test)

# 9. Evaluate the model
print("SVM Classification Results")
print("---------------------------")

print("Accuracy:", accuracy_score(y_test, y_pred))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        y_pred,
        labels=model.classes_
    )
)

print("\nClass order:", model.classes_)
