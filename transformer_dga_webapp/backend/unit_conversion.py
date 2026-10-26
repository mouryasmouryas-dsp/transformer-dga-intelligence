"""
Unit conversion for Transformer DGA Intelligence.

The model was trained on ppm (parts per million) concentrations.
This module handles conversion from supported input units to ppm.

IMPORTANT: ppm and mg/kg are not automatically interchangeable in
every context. For dissolved gases in transformer oil, the relationship
depends on the specific gas, the oil density, measurement conditions,
and the analytical method. We only support ppm as the input unit unless
a scientifically verified conversion can be established.
"""

SUPPORTED_UNITS = ["ppm"]

UNIT_DESCRIPTIONS = {
    "ppm": "Parts per million (µL/L) — the standard DGA reporting unit.",
}


def convert_to_ppm(value: float, from_unit: str) -> tuple[float, bool, str]:
    """
    Convert a gas concentration value to ppm.

    Parameters
    ----------
    value : float
        The concentration value in the source unit.
    from_unit : str
        The source unit identifier.

    Returns
    -------
    tuple of (float, bool, str)
        - Converted value in ppm
        - Whether conversion was successful
        - Description or error message
    """
    if from_unit == "ppm":
        return value, True, "No conversion needed; value is already in ppm."

    return (
        value,
        False,
        f"Conversion from '{from_unit}' to ppm is not supported. "
        f"A reliable conversion factor for dissolved gases in transformer oil "
        f"has not been established in this application. Please enter values "
        f"in ppm.",
    )


def is_unit_supported(unit: str) -> bool:
    """Check if a unit is supported for conversion."""
    return unit in SUPPORTED_UNITS
