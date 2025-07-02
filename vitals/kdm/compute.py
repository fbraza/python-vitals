from typing import Optional, TypeAlias

import bioage_params as bioage
import numpy as np
from pydantic import BaseModel

Biomarker: TypeAlias = Optional[float | None]


class KdmInput(BaseModel):
    """
    Input class for KDM (Klemera-Doubal Method) biological age calculation.

    All biomarkers are optional - KDM can be calculated with any subset of available biomarkers.
    Units should match those expected by the KDM algorithm.
    """

    albumin: Biomarker
    alkaline_phosphatase: Biomarker
    log_crp: Biomarker
    total_cholesterol: Biomarker
    log_creatinine: Biomarker
    hba1c: Biomarker
    systolic_blood_pressure: Biomarker
    blood_urea_nitrogen: Biomarker
    uric_acid: Biomarker
    lymphocyte_percent: Biomarker
    mean_cell_volume: Biomarker
    white_blood_cell_count: Biomarker
    age: float  # Chronological age is required


def kdm_age(data: KdmInput, sex: str = "male") -> tuple[float, float, float]:
    """
    Calculate biological age using the Klemera-Doubal Method (KDM).

    KDM Formula: BA = (Σᵢ [(xᵢ - qᵢ) × mᵢ/sᵢ²] + CA/s_BA²) / (Σᵢ [mᵢ²/sᵢ²] + 1/s_BA²)

    Args:
        data: KdmInput object with biomarker values and chronological age
        sex: "male" or "female" to select appropriate coefficients

    Returns:
        Tuple of (chronological_age, biological_age, age_acceleration)
    """
    # Select appropriate coefficients based on sex
    if sex.lower() == "male":
        kdm_params = bioage.KdmForMales()
    else:
        kdm_params = bioage.KdmForFemales()

    # Get input data as dictionary
    input_dict = data.model_dump()
    kdm_dict = kdm_params.model_dump()

    # Extract biomarker values and parameters for available biomarkers
    x_values = []  # biomarker values
    q_values = []  # mean/reference values
    k_values = []  # slope coefficients (m in formula)
    s_values = []  # standard deviations

    # Process each biomarker (excluding age and s_ba2)
    for field, value in input_dict.items():
        if field != "age" and value is not None and field in kdm_dict:
            x_values.append(value)
            params = kdm_dict[field]
            q_values.append(params["q"])
            k_values.append(params["k"])
            s_values.append(params["s"])

    # Convert to numpy arrays for vectorized computation
    x = np.array(x_values)
    q = np.array(q_values)
    k = np.array(k_values)
    s = np.array(s_values)

    # Compute using numpy vectorization
    # Numerator: Σᵢ [(xᵢ - qᵢ) × mᵢ/sᵢ²] + CA/s_BA²
    numerator = np.sum((x - q) * k / (s**2)) + data.age / kdm_params.s_ba2

    # Denominator: Σᵢ [mᵢ²/sᵢ²] + 1/s_BA²
    denominator = np.sum(k**2 / (s**2)) + 1 / kdm_params.s_ba2

    # Calculate biological age
    biological_age = numerator / denominator

    # Calculate age acceleration
    age_acceleration = biological_age - data.age

    return (data.age, biological_age, age_acceleration)
