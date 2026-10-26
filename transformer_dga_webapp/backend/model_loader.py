"""
Model loader for Transformer DGA Intelligence.

Handles loading the saved Random Forest model artifact and metadata,
with validation to ensure the loaded model matches expected configuration.
"""

import json
import os

import joblib

from config.settings import MODEL_DIR, CONFIG_DIR, FEATURE_NAMES, CLASS_LABELS


class ModelLoadError(Exception):
    """Raised when the model cannot be loaded or fails validation."""
    pass


def load_model():
    """
    Load the trained Random Forest model from disk.

    Returns
    -------
    model : sklearn.ensemble.RandomForestClassifier
        The fitted model.

    Raises
    ------
    ModelLoadError
        If the model file is missing, corrupt, or fails validation.
    """
    model_path = os.path.join(MODEL_DIR, "random_forest_model.joblib")

    if not os.path.exists(model_path):
        raise ModelLoadError(
            f"Model file not found: {model_path}. "
            "Run backend/train_model.py first."
        )

    try:
        model = joblib.load(model_path)
    except Exception as e:
        raise ModelLoadError(f"Failed to load model: {e}")

    # Validate the model has the expected attributes
    if not hasattr(model, "predict"):
        raise ModelLoadError("Loaded object does not have a predict method.")

    if not hasattr(model, "n_features_in_"):
        raise ModelLoadError("Loaded model has no n_features_in_ attribute.")

    if model.n_features_in_ != len(FEATURE_NAMES):
        raise ModelLoadError(
            f"Model expects {model.n_features_in_} features, "
            f"but configuration specifies {len(FEATURE_NAMES)}."
        )

    # Validate class labels
    model_classes = sorted(model.classes_.tolist())
    expected_classes = sorted(CLASS_LABELS)
    if model_classes != expected_classes:
        raise ModelLoadError(
            f"Model classes {model_classes} do not match "
            f"expected classes {expected_classes}."
        )

    return model


def load_metadata():
    """
    Load the model metadata JSON.

    Returns
    -------
    dict
        Model metadata including training stats, metrics, and configuration.

    Raises
    ------
    ModelLoadError
        If the metadata file is missing or corrupt.
    """
    metadata_path = os.path.join(CONFIG_DIR, "model_metadata.json")

    if not os.path.exists(metadata_path):
        raise ModelLoadError(
            f"Metadata file not found: {metadata_path}. "
            "Run backend/train_model.py first."
        )

    try:
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
    except Exception as e:
        raise ModelLoadError(f"Failed to load metadata: {e}")

    return metadata


def get_model_version():
    """Return the model version string."""
    try:
        metadata = load_metadata()
        return metadata.get("model_version", "unknown")
    except ModelLoadError:
        return "not available"


# Alias for backward compatibility
get_model_metadata = load_metadata

