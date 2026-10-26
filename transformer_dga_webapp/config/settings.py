"""
Model metadata configuration for Transformer DGA Intelligence.

This file stores the exact model configuration, feature order, class labels,
and evaluation metrics from the original PRML project. All values are sourced
from the actual project scripts and saved CSV results.
"""

import json
import os

# ─── Paths ───────────────────────────────────────────────────────────────────
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(APP_DIR, "models")
CONFIG_DIR = os.path.join(APP_DIR, "config")
ASSETS_DIR = os.path.join(APP_DIR, "assets")
DATA_DIR = os.path.dirname(APP_DIR)  # Parent = TRANSFORMER PROJECT folder

# ─── Dataset ─────────────────────────────────────────────────────────────────
DATASET_FILENAME = "IEEE_STANDARD.xlsx"
DATASET_PATH = os.path.join(DATA_DIR, DATASET_FILENAME)
TARGET_COLUMN_ORIGINAL = "故障类型"
TARGET_COLUMN = "Fault Type"

# ─── Feature configuration ───────────────────────────────────────────────────
# Exact order used in all training scripts
FEATURE_NAMES = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]

FEATURE_LABELS = {
    "H2": "H₂ — Hydrogen",
    "CH4": "CH₄ — Methane",
    "C2H6": "C₂H₆ — Ethane",
    "C2H4": "C₂H₄ — Ethylene",
    "C2H2": "C₂H₂ — Acetylene",
}

FEATURE_FORMULAS = {
    "H2": "H₂",
    "CH4": "CH₄",
    "C2H6": "C₂H₆",
    "C2H4": "C₂H₄",
    "C2H2": "C₂H₂",
}

# ─── Class labels (verified from dataset) ────────────────────────────────────
CLASS_LABELS = ["D1", "D2", "PD", "T1", "T2", "T3"]

CLASS_DESCRIPTIONS = {
    "PD": {
        "name": "Partial Discharge",
        "category": "Electrical",
        "description": (
            "Partial discharge involves localised electrical discharges that "
            "do not fully bridge the insulation gap. These can occur in gas "
            "cavities, at interfaces, or in regions of high electric field "
            "stress within the transformer insulation system."
        ),
        "dga_context": (
            "PD is often associated with elevated hydrogen (H₂) levels. "
            "Other gases may remain relatively low compared to discharge "
            "or thermal fault categories."
        ),
        "engineering_note": (
            "A PD prediction warrants further investigation using partial "
            "discharge measurement instruments and visual inspection of "
            "accessible insulation surfaces. PD can progress over time."
        ),
    },
    "D1": {
        "name": "Low-Energy Discharge",
        "category": "Electrical",
        "description": (
            "Low-energy discharges include small arcs, sparking, or tracking "
            "events. These may be caused by poor connections, floating "
            "components, or breakdown of insulating barriers under moderate "
            "electrical stress."
        ),
        "dga_context": (
            "D1 faults may produce hydrogen and acetylene (C₂H₂), though "
            "at lower levels than high-energy discharge events."
        ),
        "engineering_note": (
            "Investigate potential sources of sparking, poor contacts, or "
            "tracking paths. A D1 prediction does not confirm the exact "
            "location or severity of the discharge."
        ),
    },
    "D2": {
        "name": "High-Energy Discharge",
        "category": "Electrical",
        "description": (
            "High-energy discharges involve significant arcing or flashover "
            "events. These represent more severe electrical faults that can "
            "cause substantial insulation damage and may progress rapidly."
        ),
        "dga_context": (
            "D2 faults are typically associated with significant acetylene "
            "(C₂H₂) and ethylene (C₂H₄) production. Hydrogen may also be "
            "elevated."
        ),
        "engineering_note": (
            "A D2 prediction suggests a potentially serious condition. "
            "Prompt engineering assessment is recommended. Inspect for "
            "evidence of arcing damage, carbonisation, or metal particles."
        ),
    },
    "T1": {
        "name": "Thermal Fault < 300 °C",
        "category": "Thermal",
        "description": (
            "Low-temperature thermal faults involve localised overheating "
            "below approximately 300 °C. These may be caused by circulating "
            "currents, blocked oil flow, or hot spots on structural components."
        ),
        "dga_context": (
            "T1 faults may show modest increases in methane (CH₄) and "
            "ethane (C₂H₆) with limited ethylene production."
        ),
        "engineering_note": (
            "Investigate potential sources of localised overheating. Monitor "
            "gas trends over time. A single T1 prediction does not establish "
            "the exact hot-spot location or temperature."
        ),
    },
    "T2": {
        "name": "Thermal Fault 300–700 °C",
        "category": "Thermal",
        "description": (
            "Medium-temperature thermal faults involve overheating in the "
            "range of approximately 300 °C to 700 °C. This may indicate "
            "significant hot spots on conductors, connections, or core "
            "components."
        ),
        "dga_context": (
            "T2 faults may produce notable ethylene (C₂H₄) and ethane "
            "(C₂H₆) concentrations, with the ethylene-to-ethane ratio "
            "potentially increasing with temperature."
        ),
        "engineering_note": (
            "A T2 prediction suggests meaningful thermal stress. Review "
            "load conditions, cooling system performance, and connection "
            "integrity. Thermal imaging may help locate hot spots."
        ),
    },
    "T3": {
        "name": "Thermal Fault > 700 °C",
        "category": "Thermal",
        "description": (
            "High-temperature thermal faults involve severe overheating "
            "above approximately 700 °C. This may indicate critical hot "
            "spots, possibly involving conductor or core damage."
        ),
        "dga_context": (
            "T3 faults typically produce significant ethylene (C₂H₄) "
            "concentrations. Methane and ethane may also be elevated, "
            "and some hydrogen may be present."
        ),
        "engineering_note": (
            "A T3 prediction suggests a potentially critical thermal "
            "condition. Urgent engineering assessment is recommended. "
            "Consider de-energising the transformer if confirmed by "
            "additional diagnostic evidence."
        ),
    },
}

# ─── Model configuration (from random_forest.py and compare_models.py) ──────
MODEL_CONFIG = {
    "algorithm": "Random Forest",
    "n_estimators": 100,
    "max_depth": None,
    "min_samples_leaf": 2,
    "class_weight": "balanced",
    "random_state": 42,
    "version": "1.0.0",
    "training_unit": "ppm",
    "preprocessing": "none",  # RF trained on raw ppm, no StandardScaler
    "train_test_split": {
        "test_size": 0.20,
        "random_state": 42,
        "stratify": True,
    },
    "grid_search": {
        "n_estimators": [100, 200],
        "max_depth": [None, 10, 20],
        "min_samples_leaf": [1, 2, 4],
        "scoring": "f1_macro",
        "cv_folds": 5,
    },
}

# ─── Recorded evaluation metrics (from project_results.py / CSVs) ───────────
MODEL_COMPARISON = [
    {"Model": "Gaussian Naive Bayes", "Accuracy": 41.53, "Macro F1": 0.3293},
    {"Model": "Logistic Regression", "Accuracy": 48.31, "Macro F1": 0.3284},
    {"Model": "Initial SVM", "Accuracy": 28.81, "Macro F1": 0.1270},
    {"Model": "Tuned SVM", "Accuracy": 64.41, "Macro F1": 0.5544},
    {"Model": "Random Forest", "Accuracy": 75.42, "Macro F1": 0.7382},
]

GROUPED_VALIDATION = {
    "mean_accuracy": 0.7751,
    "accuracy_std": 0.0151,
    "mean_macro_f1": 0.7678,
    "macro_f1_std": 0.0156,
}

PERMUTATION_IMPORTANCE = [
    {"Gas": "C2H4", "Mean_Importance": 0.3534, "Fold_Std": 0.0128},
    {"Gas": "C2H2", "Mean_Importance": 0.3202, "Fold_Std": 0.0208},
    {"Gas": "H2", "Mean_Importance": 0.1865, "Fold_Std": 0.0381},
    {"Gas": "C2H6", "Mean_Importance": 0.1225, "Fold_Std": 0.0188},
    {"Gas": "CH4", "Mean_Importance": 0.0504, "Fold_Std": 0.0287},
]

# ─── Tooltip / help text ─────────────────────────────────────────────────────
TOOLTIPS = {
    "H2": (
        "Hydrogen is one of the gases measured during dissolved gas analysis. "
        "Its concentration can contribute to transformer fault interpretation. "
        "This model uses it together with four other gas measurements."
    ),
    "CH4": (
        "Methane is a hydrocarbon gas that can be generated by thermal "
        "decomposition of insulating oil. Its level relative to other gases "
        "helps characterise fault type and temperature."
    ),
    "C2H6": (
        "Ethane is generated during moderate thermal degradation of "
        "transformer oil. It contributes to distinguishing between different "
        "thermal fault severity levels."
    ),
    "C2H4": (
        "Ethylene is a measured dissolved gas that can contribute to the "
        "interpretation of thermal conditions in oil-filled transformers. "
        "It has the highest permutation importance in this model."
    ),
    "C2H2": (
        "Acetylene is a key indicator gas for electrical discharge faults. "
        "Its presence often signals arcing or high-energy electrical events "
        "within the transformer."
    ),
    "concentration_unit": (
        "Choose the unit shown on your laboratory report. The model was "
        "trained on ppm (parts per million) data. If you select a different "
        "supported unit, the application will convert your values before "
        "prediction."
    ),
    "analyse_button": (
        "Validate your five gas measurements and submit them to the trained "
        "Random Forest model to obtain an experimental fault-class prediction."
    ),
    "accuracy": (
        "Accuracy is the fraction of evaluated samples classified correctly. "
        "It does not guarantee the same performance on a new transformer or "
        "a different dataset."
    ),
    "macro_f1": (
        "Macro F1 calculates the F1-score for each class and then averages "
        "the six class scores equally. It helps reveal poor performance on "
        "less frequent fault categories."
    ),
    "grouped_cv": (
        "This evaluation keeps identical five-gas measurement vectors in the "
        "same fold. It reduces one form of repeated-input leakage but does "
        "not establish performance on independent transformers."
    ),
    "feature_importance": (
        "This value estimates how much the model's predictive performance "
        "decreases when a feature is shuffled. It does not establish that "
        "the gas physically causes a fault."
    ),
    "predicted_class": (
        "This is the class returned by the trained machine-learning model. "
        "It is an experimental prediction, not a confirmed physical diagnosis."
    ),
    "model_probability": (
        "This is a probability estimate produced by the model. It should not "
        "be interpreted as a guarantee of diagnostic correctness or as a "
        "calibrated probability unless calibration has been verified."
    ),
    "download_pdf": (
        "Download a record of the submitted gas values, predicted class, "
        "model information, charts, and limitations. The report is not a "
        "certified transformer condition assessment."
    ),
    "precision": (
        "Precision measures how many of the samples predicted as a given "
        "class actually belong to that class. Higher precision means fewer "
        "false positives for that category."
    ),
    "recall": (
        "Recall measures how many of the actual samples of a given class "
        "were correctly identified. Higher recall means fewer missed cases "
        "for that category."
    ),
    "f1_score": (
        "F1-score is the harmonic mean of precision and recall. It balances "
        "both metrics and is especially useful when class sizes are unequal."
    ),
    "confusion_matrix": (
        "A confusion matrix shows how many samples of each actual class were "
        "predicted as each class. Diagonal entries represent correct "
        "predictions; off-diagonal entries are misclassifications."
    ),
}

# ─── Demonstration sample ────────────────────────────────────────────────────
DEMO_SAMPLES = {
    "Thermal fault example": {
        "H2": 120.0,
        "CH4": 250.0,
        "C2H6": 85.0,
        "C2H4": 410.0,
        "C2H2": 5.0,
        "description": (
            "Illustrative gas readings with elevated ethylene, suggesting "
            "a thermal fault pattern. These are sample values for "
            "demonstration purposes only."
        ),
    },
    "Discharge fault example": {
        "H2": 350.0,
        "CH4": 45.0,
        "C2H6": 12.0,
        "C2H4": 30.0,
        "C2H2": 180.0,
        "description": (
            "Illustrative gas readings with elevated acetylene, suggesting "
            "a discharge fault pattern. These are sample values for "
            "demonstration purposes only."
        ),
    },
    "Partial discharge example": {
        "H2": 890.0,
        "CH4": 15.0,
        "C2H6": 8.0,
        "C2H4": 5.0,
        "C2H2": 3.0,
        "description": (
            "Illustrative gas readings dominated by hydrogen, suggesting "
            "a partial discharge pattern. These are sample values for "
            "demonstration purposes only."
        ),
    },
}
