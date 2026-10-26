"""
Prediction backend for Transformer DGA Intelligence.

Implements the end-to-end inference pipeline:
1. Validate inputs
2. Convert units (if needed)
3. Arrange features in training order
4. Run the trained model
5. Return structured results with warnings
"""

import datetime
import uuid

import numpy as np
import pandas as pd

from config.settings import (
    FEATURE_NAMES,
    FEATURE_LABELS,
    CLASS_DESCRIPTIONS,
    MODEL_CONFIG,
)
from backend.model_loader import load_model, load_metadata, get_model_version
from backend.validation import validate_gas_inputs, validate_unit
from backend.unit_conversion import convert_to_ppm


class PredictionResult:
    """Structured result from a prediction."""

    def __init__(self):
        self.success: bool = False
        self.reference_id: str = ""
        self.timestamp: str = ""
        self.predicted_class: str = ""
        self.class_description: dict = {}
        self.probabilities: dict = {}
        self.gas_values_input: dict = {}
        self.gas_values_model: dict = {}
        self.input_unit: str = ""
        self.model_unit: str = "ppm"
        self.model_version: str = ""
        self.transformer_label: str = ""
        self.user_name: str = ""
        self.errors: list[str] = []
        self.warnings: list[str] = []


def predict_transformer_fault(
    gas_values: dict[str, float],
    unit: str = "ppm",
    transformer_label: str = "",
    user_name: str = "",
) -> PredictionResult:
    """
    Run the full inference pipeline.

    Parameters
    ----------
    gas_values : dict
        Five gas concentrations keyed by feature name.
    unit : str
        The concentration unit of the input values.
    transformer_label : str
        Optional transformer identification label.
    user_name : str
        Optional user name for the report.

    Returns
    -------
    PredictionResult
        Complete structured result including prediction, probabilities,
        warnings, and metadata.
    """
    result = PredictionResult()
    result.reference_id = f"DGA-{uuid.uuid4().hex[:8].upper()}"
    result.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result.input_unit = unit
    result.transformer_label = transformer_label
    result.user_name = user_name
    result.gas_values_input = dict(gas_values)

    # 1. Validate unit
    unit_check = validate_unit(unit)
    if not unit_check.is_valid:
        result.errors.extend(unit_check.errors)
        return result

    # 2. Load metadata for training stats
    try:
        metadata = load_metadata()
        train_stats = metadata.get("train_data_stats", None)
    except Exception:
        train_stats = None

    # 3. Validate gas inputs
    input_check = validate_gas_inputs(gas_values, train_stats)
    if not input_check.is_valid:
        result.errors.extend(input_check.errors)
        return result
    result.warnings.extend(input_check.warnings)

    # 4. Convert units to ppm (model training unit)
    model_values = {}
    for gas in FEATURE_NAMES:
        raw_value = float(gas_values[gas])
        converted, success, msg = convert_to_ppm(raw_value, unit)
        if not success:
            result.errors.append(msg)
            return result
        model_values[gas] = converted

    result.gas_values_model = model_values

    # 5. Load model
    try:
        model = load_model()
    except Exception as e:
        result.errors.append(
            f"The trained model could not be loaded. "
            f"No prediction has been generated. Error: {e}"
        )
        return result

    # 6. Arrange features in the exact training order with feature names
    feature_df = pd.DataFrame(
        [[model_values[gas] for gas in FEATURE_NAMES]],
        columns=FEATURE_NAMES,
    )

    # 7. Predict
    try:
        predicted_class = model.predict(feature_df)[0]
    except Exception as e:
        result.errors.append(
            f"Prediction failed: {e}. "
            "This may indicate a data format issue."
        )
        return result

    result.predicted_class = predicted_class
    result.class_description = CLASS_DESCRIPTIONS.get(predicted_class, {})

    # 8. Get probability estimates if available
    if hasattr(model, "predict_proba"):
        try:
            probas = model.predict_proba(feature_df)[0]
            classes = model.classes_
            result.probabilities = {
                str(cls): float(prob) for cls, prob in zip(classes, probas)
            }
        except Exception:
            result.warnings.append(
                "Probability estimates could not be computed. "
                "Only the predicted class is available."
            )

    # 9. Model version
    result.model_version = get_model_version()
    result.success = True

    return result
