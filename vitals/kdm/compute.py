import json
from typing import TypeAlias

import numpy as np
from biomarkers import helpers, schemas
from pydantic import BaseModel

KdmParameters: TypeAlias = dict[str, float]


class KdmForMales(BaseModel):
    """
    KDM (Klemera-Doubal Method) model parameters for males from the BioAge paper.

    KDM Formula: Biological age = (Σᵢ [(xᵢ - qᵢ) × mᵢ/sᵢ²] + CA/s_BA²) / (Σᵢ [mᵢ²/sᵢ²] + 1/s_BA²)

    Where:
    - xᵢ: biomarker value
    - qᵢ: biomarker mean/reference value (parameter 'q')
    - mᵢ: slope coefficient (parameter 'k')
    - sᵢ: biomarker standard deviation (parameter 's')
    - CA: chronological age
    - s_BA²: biological age variance (s_ba2 field)

    Additional parameters (r, r1, r2, n2) are correlation and variance terms from the BioAge implementation.
    """

    s_ba2: float = 2079.825
    albumin: KdmParameters = {
        "q": 4.5770191,
        "k": -0.007252060,
        "s": 0.34322125,
        "r": 0.0777039952,
        "r1": 5.889913e-03,
        "r2": 0.021129402,
        "n2": 4.464516e-04,
    }
    alkaline_phosphatase: KdmParameters = {
        "q": 76.0370610,
        "k": 0.222890703,
        "s": 25.49204603,
        "r": 0.0142124841,
        "r1": 1.042371e-03,
        "r2": 0.008743539,
        "n2": 7.644948e-05,
    }
    log_crp: KdmParameters = {
        "q": 0.1549751,
        "k": 0.002781679,
        "s": 0.21907599,
        "r": 0.0295113073,
        "r1": 2.181255e-03,
        "r2": 0.012697326,
        "n2": 1.612221e-04,
    }
    total_cholesterol: KdmParameters = {
        "q": 190.3257889,
        "k": 0.384942117,
        "s": 40.85123580,
        "r": 0.0165064839,
        "r1": 1.210647e-03,
        "r2": 0.009423023,
        "n2": 8.879335e-05,
    }
    log_creatinine: KdmParameters = {
        "q": 0.5874157,
        "k": 0.001580101,
        "s": 0.09771588,
        "r": 0.0470147839,
        "r1": 3.506203e-03,
        "r2": 0.016170364,
        "n2": 2.614807e-04,
    }
    hba1c: KdmParameters = {
        "q": 4.7315111,
        "k": 0.017329423,
        "s": 0.92103000,
        "r": 0.0629310125,
        "r1": 4.720007e-03,
        "r2": 0.018815264,
        "n2": 3.540142e-04,
    }
    systolic_blood_pressure: KdmParameters = {
        "q": 101.0896520,
        "k": 0.557382604,
        "s": 15.87772546,
        "r": 0.1887707743,
        "r1": 1.525220e-02,
        "r2": 0.035104688,
        "n2": 1.232339e-03,
    }
    blood_urea_nitrogen: KdmParameters = {
        "q": 10.1076356,
        "k": 0.101132960,
        "s": 4.82743955,
        "r": 0.0763786608,
        "r1": 5.789778e-03,
        "r2": 0.020949607,
        "n2": 4.388860e-04,
    }
    uric_acid: KdmParameters = {
        "q": 5.9429652,
        "k": 0.002664833,
        "s": 1.37239218,
        "r": 0.0007107763,
        "r1": 5.176762e-05,
        "r2": 0.001941743,
        "n2": 3.770366e-06,
    }
    lymphocyte_percent: KdmParameters = {
        "q": 37.5509570,
        "k": -0.093601372,
        "s": 8.60390248,
        "r": 0.0218990508,
        "r1": 1.609902e-03,
        "r2": 0.010878944,
        "n2": 1.183514e-04,
    }
    mean_cell_volume: KdmParameters = {
        "q": 87.7220636,
        "k": 0.047325418,
        "s": 5.22194207,
        "r": 0.0153018330,
        "r1": 1.121074e-03,
        "r2": 0.009062800,
        "n2": 8.213435e-05,
    }
    white_blood_cell_count: KdmParameters = {
        "q": 7.0596687,
        "k": 0.001751592,
        "s": 2.11201120,
        "r": 0.0001301107,
        "r1": 9.460049e-06,
        "r2": 0.000829348,
        "n2": 6.878182e-07,
    }


class KdmForFemales(BaseModel):
    """
    KDM (Klemera-Doubal Method) model parameters for females from the BioAge paper.

    KDM Formula: Biological age = (Σᵢ [(xᵢ - qᵢ) × mᵢ/sᵢ²] + CA/s_BA²) / (Σᵢ [mᵢ²/sᵢ²] + 1/s_BA²)

    Where:
    - xᵢ: biomarker value
    - qᵢ: biomarker mean/reference value (parameter 'q')
    - mᵢ: slope coefficient (parameter 'k')
    - sᵢ: biomarker standard deviation (parameter 's')
    - CA: chronological age
    - s_BA²: biological age variance (s_ba2 field)

    Additional parameters (r, r1, r2, n2) are correlation and variance terms from the BioAge implementation.
    """

    s_ba2: float = 1459.997
    albumin: KdmParameters = {
        "q": 4.1570748,
        "k": -0.002187197,
        "s": 0.34273867,
        "r": 0.0075274130,
        "r1": 5.536657e-04,
        "r2": 0.006381529,
        "n2": 4.072391e-05,
    }
    alkaline_phosphatase: KdmParameters = {
        "q": 54.9583759,
        "k": 0.629927313,
        "s": 27.88257433,
        "r": 0.0868189733,
        "r1": 6.656791e-03,
        "r2": 0.022592150,
        "n2": 5.104053e-04,
    }
    log_crp: KdmParameters = {
        "q": 0.3032893,
        "k": 0.001177600,
        "s": 0.27996081,
        "r": 0.0032849563,
        "r1": 2.410822e-04,
        "r2": 0.004206302,
        "n2": 1.769297e-05,
    }
    total_cholesterol: KdmParameters = {
        "q": 146.3495243,
        "k": 1.314791516,
        "s": 41.22743392,
        "r": 0.1596301359,
        "r1": 1.274172e-02,
        "r2": 0.031891180,
        "n2": 1.017047e-03,
    }
    log_creatinine: KdmParameters = {
        "q": 0.4669501,
        "k": 0.001734239,
        "s": 0.08818555,
        "r": 0.0671666531,
        "r1": 5.096692e-03,
        "r2": 0.019665795,
        "n2": 3.867435e-04,
    }
    hba1c: KdmParameters = {
        "q": 4.4497929,
        "k": 0.022953617,
        "s": 1.01177362,
        "r": 0.0877771017,
        "r1": 6.721379e-03,
        "r2": 0.022686514,
        "n2": 5.146779e-04,
    }
    systolic_blood_pressure: KdmParameters = {
        "q": 85.5113809,
        "k": 0.796155042,
        "s": 16.84589168,
        "r": 0.2922805799,
        "r1": 2.555075e-02,
        "r2": 0.047261080,
        "n2": 2.233610e-03,
    }
    blood_urea_nitrogen: KdmParameters = {
        "q": 6.1935696,
        "k": 0.144843570,
        "s": 4.23475788,
        "r": 0.1786476236,
        "r1": 1.445670e-02,
        "r2": 0.034203507,
        "n2": 1.169880e-03,
    }
    uric_acid: KdmParameters = {
        "q": 3.5346439,
        "k": 0.025099998,
        "s": 1.29280630,
        "r": 0.0656020854,
        "r1": 4.972778e-03,
        "r2": 0.019415127,
        "n2": 3.769471e-04,
    }
    lymphocyte_percent: KdmParameters = {
        "q": 34.7335678,
        "k": -0.016095247,
        "s": 8.56682559,
        "r": 0.0006586207,
        "r1": 4.821647e-05,
        "r2": 0.001878788,
        "n2": 3.529843e-06,
    }
    mean_cell_volume: KdmParameters = {
        "q": 86.2748177,
        "k": 0.051379381,
        "s": 5.78871799,
        "r": 0.0145084795,
        "r1": 1.069098e-03,
        "r2": 0.008875779,
        "n2": 7.877945e-05,
    }
    white_blood_cell_count: KdmParameters = {
        "q": 7.5436795,
        "k": -0.007737116,
        "s": 2.13408561,
        "r": 0.0024468377,
        "r1": 1.793370e-04,
        "r2": 0.003625495,
        "n2": 1.314421e-05,
    }


def biological_age(filepath: str) -> tuple[float, float, float]:
    """
    Calculate biological age using the Klemera-Doubal Method (KDM) from a JSON file.

    Args:
        filepath: Path to JSON file containing biomarker data

    Returns:
        Tuple of (chronological_age, biological_age, age_acceleration)
    """
    # Extract biomarkers from JSON file
    biomarkers = helpers.extract_biomarkers_from_json(
        filepath=filepath,
        biomarker_class=schemas.KdmMarkers,
        biomarker_units=schemas.KdmUnits(),
    )

    if not isinstance(biomarkers, schemas.KdmMarkers):
        raise ValueError("Invalid biomarkers data")

    # Get sex from metadata if needed (for now defaulting to male)
    with open(filepath) as f:
        json_data = json.load(f)
    metadata = json_data.get("metadata", {})
    sex = metadata.get("sex", "male")

    return __klemera_doubal(biomarkers, sex)


def __klemera_doubal(
    data: schemas.KdmMarkers, sex: str = "male"
) -> tuple[float, float, float]:
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
    kdm_params: KdmForMales | KdmForFemales = (
        KdmForMales() if sex.lower() == "male" else KdmForFemales()
    )

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
        if field != "age" and value is not None:
            # Check if this biomarker needs log transformation
            if field == "crp" and "log_crp" in kdm_dict:
                # Use log transformation for CRP
                x_values.append(np.log(value))
                params = kdm_dict["log_crp"]
                q_values.append(params["q"])
                k_values.append(params["k"])
                s_values.append(params["s"])
            elif field == "creatinine" and "log_creatinine" in kdm_dict:
                # Use log transformation for creatinine
                x_values.append(np.log(value))
                params = kdm_dict["log_creatinine"]
                q_values.append(params["q"])
                k_values.append(params["k"])
                s_values.append(params["s"])
            elif field in kdm_dict:
                # Regular biomarker
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
