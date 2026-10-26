"""
Input validation for Transformer DGA Intelligence.

Validates user-entered gas concentration values before passing
them to the prediction backend. Returns structured error/warning
messages for the frontend to display.
"""

import math
from typing import Any

from config.settings import FEATURE_NAMES, FEATURE_LABELS


class ValidationResult:
    """Container for validation outcomes."""

    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.is_valid: bool = True

    def add_error(self, message: str):
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str):
        self.warnings.append(message)


def validate_gas_inputs(
    gas_values: dict[str, Any],
    train_stats: dict | None = None,
) -> ValidationResult:
    """
    Validate a dictionary of gas concentration values.

    Parameters
    ----------
    gas_values : dict
        Keys are gas names (H2, CH4, etc.), values are user-entered values.
    train_stats : dict, optional
        Training data statistics for out-of-distribution detection.

    Returns
    -------
    ValidationResult
        Contains errors (invalid) and warnings (unusual but accepted).
    """
    result = ValidationResult()

    # Check all required features are present
    for gas in FEATURE_NAMES:
        if gas not in gas_values:
            result.add_error(
                f"{FEATURE_LABELS[gas]}: This field is required. "
                "Enter the gas concentration from your laboratory report."
            )

    if not result.is_valid:
        return result

    # Validate each gas value
    for gas in FEATURE_NAMES:
        value = gas_values[gas]
        label = FEATURE_LABELS[gas]

        # Check for None / empty
        if value is None or (isinstance(value, str) and value.strip() == ""):
            result.add_error(
                f"{label}: This field is empty. "
                "Enter the gas concentration shown on your laboratory report."
            )
            continue

        # Try to convert to float
        try:
            numeric_value = float(value)
        except (ValueError, TypeError):
            result.add_error(
                f"{label}: '{value}' is not a valid number. "
                "Enter a numeric concentration value."
            )
            continue

        # Check for NaN
        if math.isnan(numeric_value):
            result.add_error(
                f"{label}: The value is not a number (NaN). "
                "Enter a valid numeric concentration."
            )
            continue

        # Check for infinity
        if math.isinf(numeric_value):
            result.add_error(
                f"{label}: Infinite values are not accepted. "
                "Enter a finite concentration value."
            )
            continue

        # Check for negative values
        if numeric_value < 0:
            result.add_error(
                f"{label}: Negative concentrations ({numeric_value}) "
                "are not accepted. Check the original measurement."
            )
            continue

        # Check for implausibly large values (>100,000 ppm as a soft limit)
        if numeric_value > 100_000:
            result.add_warning(
                f"{label}: The value {numeric_value:,.1f} ppm is unusually high. "
                "Please verify the measurement. The model may produce "
                "unreliable predictions for values this far above the "
                "training data range."
            )

        # Check against training data range if stats are available
        if train_stats and gas in train_stats:
            stats = train_stats[gas]
            train_max = stats.get("max", float("inf"))
            train_min = stats.get("min", 0)

            if numeric_value > train_max * 1.5:
                result.add_warning(
                    f"{label}: {numeric_value:,.1f} ppm exceeds the "
                    f"training data maximum ({train_max:,.1f} ppm) by a "
                    "significant margin. The prediction may be unreliable."
                )
            elif numeric_value > train_max:
                result.add_warning(
                    f"{label}: {numeric_value:,.1f} ppm is above the "
                    f"training data maximum ({train_max:,.1f} ppm). "
                    "The prediction may be less reliable."
                )

    return result


def validate_unit(unit: str) -> ValidationResult:
    """Validate the selected concentration unit."""
    result = ValidationResult()
    supported = ["ppm"]

    if unit not in supported:
        result.add_error(
            f"Unit '{unit}' is not supported. The model was trained on ppm "
            "data, and a reliable conversion from '{unit}' has not been "
            "established. Please enter values in ppm."
        )

    return result
