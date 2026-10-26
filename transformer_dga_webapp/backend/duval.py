"""
Duval Triangle 1 Analysis Module
================================
Implements classical Duval Triangle 1 fault classification
according to IEEE C57.104 and IEC 60599 standards.
Gases: %CH4, %C2H4, %C2H2
"""

from typing import Dict, Any, Tuple


def calculate_duval_triangle_1(ch4: float, c2h4: float, c2h2: float) -> Dict[str, Any]:
    """
    Calculate Duval Triangle 1 coordinates and fault zone.

    Parameters
    ----------
    ch4 : float
        Methane concentration in ppm.
    c2h4 : float
        Ethylene concentration in ppm.
    c2h2 : float
        Acetylene concentration in ppm.

    Returns
    -------
    dict
        Contains %CH4, %C2H4, %C2H2, zone code, zone name, and description.
    """
    total = float(ch4) + float(c2h4) + float(c2h2)

    if total <= 0:
        return {
            "valid": False,
            "pct_ch4": 0.0,
            "pct_c2h4": 0.0,
            "pct_c2h2": 0.0,
            "zone": "N/A",
            "zone_name": "Insufficient Gas",
            "description": "Sum of CH4, C2H4, and C2H2 is zero. Duval Triangle 1 cannot be computed.",
        }

    pct_ch4 = (float(ch4) / total) * 100.0
    pct_c2h4 = (float(c2h4) / total) * 100.0
    pct_c2h2 = (float(c2h2) / total) * 100.0

    # Duval Triangle 1 standard geometric boundaries (IEC 60599 / IEEE C57.104)
    zone = "Unknown"
    zone_name = "Undetermined"
    description = ""

    # PD: Partial Discharge (%CH4 >= 98%)
    if pct_ch4 >= 98.0:
        zone = "PD"
        zone_name = "Partial Discharge"
        description = "Corona, voids in solid insulation, or localized low-energy gas ionization."

    # T1: Thermal fault < 300 °C (%CH4 < 98% and %C2H2 < 4% and %C2H4 < 20%)
    elif pct_c2h2 < 4.0 and pct_c2h4 < 20.0:
        zone = "T1"
        zone_name = "Thermal Fault < 300 °C"
        description = "Low-temperature overheating of insulation paper, core hot spots."

    # T2: Thermal fault 300 °C - 700 °C (%C2H2 < 4% and 20% <= %C2H4 < 50%)
    elif pct_c2h2 < 4.0 and 20.0 <= pct_c2h4 < 50.0:
        zone = "T2"
        zone_name = "Thermal Fault 300 °C - 700 °C"
        description = "Medium-temperature thermal overheating of oil, windings, or core joints."

    # T3: Thermal fault > 700 °C (%C2H2 < 15% and %C2H4 >= 50%)
    elif pct_c2h2 < 15.0 and pct_c2h4 >= 50.0:
        zone = "T3"
        zone_name = "Thermal Fault > 700 °C"
        description = "Severe high-temperature thermal fault; conductor melting, severe localized hot spots."

    # D1: Low energy discharge
    elif (pct_c2h2 >= 13.0 and pct_c2h2 < 29.0 and pct_c2h4 < 23.0) or (pct_c2h2 >= 4.0 and pct_c2h2 < 13.0 and pct_c2h4 >= (pct_c2h2 - 4.0)):
        zone = "D1"
        zone_name = "Low-Energy Discharge"
        description = "Sparking, tracking, breakdown of oil between floating parts or poor connections."

    # D2: High energy discharge
    elif pct_c2h2 >= 29.0 or (pct_c2h2 >= 13.0 and pct_c2h4 >= 23.0 and pct_c2h4 < 50.0):
        zone = "D2"
        zone_name = "High-Energy Discharge"
        description = "High-energy electrical arcing, flashover, or power-frequency short circuits."

    # Fallback heuristics for transitional boundary zones
    elif pct_c2h2 >= 4.0:
        if pct_c2h4 >= 40.0:
            zone = "D2"
            zone_name = "High-Energy Discharge (Arcing)"
            description = "High acetylene with elevated ethylene indicates severe electrical arcing."
        else:
            zone = "D1"
            zone_name = "Low-Energy Discharge (Sparking)"
            description = "Discharge zone with moderate acetylene."
    else:
        if pct_c2h4 >= 50.0:
            zone = "T3"
            zone_name = "Thermal Fault > 700 °C"
            description = "Severe thermal overheating."
        elif pct_c2h4 >= 20.0:
            zone = "T2"
            zone_name = "Thermal Fault 300 °C - 700 °C"
            description = "Medium thermal overheating."
        else:
            zone = "T1"
            zone_name = "Thermal Fault < 300 °C"
            description = "Low-temperature thermal fault."

    return {
        "valid": True,
        "pct_ch4": round(pct_ch4, 2),
        "pct_c2h4": round(pct_c2h4, 2),
        "pct_c2h2": round(pct_c2h2, 2),
        "zone": zone,
        "zone_name": zone_name,
        "description": description,
    }
