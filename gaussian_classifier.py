
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# 1. Load dataset
df = pd.read_excel(
    r"C:\Users\india\OneDrive\Desktop\TRANSFORMER PROJECT\IEEE_STANDARD.xlsx"
)

df = df.rename(columns={"故障类型": "Fault Type"})
df = df.drop_duplicates().reset_index(drop=True)

# 2. Select input features and target
gases = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]

X = df[gases].to_numpy(dtype=float)
y = df["Fault Type"].to_numpy()

# 3. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# 4. Gaussian Naive Bayes implemented from scratch
class GaussianNaiveBayes:

    def fit(self, X, y):
        self.classes = np.unique(y)
        self.means = {}
        self.variances = {}
        self.priors = {}

        for c in self.classes:
            X_class = X[y == c]

            self.means[c] = np.mean(X_class, axis=0)

            self.variances[c] = (
                np.var(X_class, axis=0) + 1e-9
            )

            self.priors[c] = len(X_class) / len(X)

    def predict(self, X):
        predictions = []

        for sample in X:
            log_scores = []

            for c in self.classes:
                mean = self.means[c]
                var = self.variances[c]

                # Log prior probability
                score = np.log(self.priors[c])

                # Gaussian log likelihood for each feature
                score += np.sum(
                    -0.5 * np.log(2 * np.pi * var)
                    - ((sample - mean) ** 2) / (2 * var)
                )

                log_scores.append(score)

            predictions.append(
                self.classes[np.argmax(log_scores)]
            )

        return np.array(predictions)


# 5. Train the classifier
model = GaussianNaiveBayes()
model.fit(X_train, y_train)

# 6. Predict test labels
y_pred = model.predict(X_test)

# 7. Evaluate performance
print("Gaussian Naive Bayes Results")
print("----------------------------")

print("Accuracy:", accuracy_score(y_test, y_pred))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        labels=model.classes,
        zero_division=0
    )
)

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        y_pred,
        labels=model.classes
    )
)

print("\nClass order:", model.classes)
