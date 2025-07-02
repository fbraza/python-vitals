from typing import Optional, TypeAlias

import coefficients as coef
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
        kdm_params = coef.KdmForMales()
    else:
        kdm_params = coef.KdmForFemales()

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


if __name__ == "__main__":
    # Test data from first two patients in NHANES3 dataset
    # Patient 1: 48-year-old female (gender=2)
    patient1_full = KdmInput(
        albumin=4.0,
        alkaline_phosphatase=59.0,
        log_crp=0.1906203542,  # lncrp column
        total_cholesterol=236.0,
        log_creatinine=0.4599533006,  # lncreat column
        hba1c=5.300000191,
        systolic_blood_pressure=131.0,
        blood_urea_nitrogen=14.0,
        uric_acid=5.0,  # uap column
        lymphocyte_percent=32.34999847,
        mean_cell_volume=92.40000153,
        white_blood_cell_count=4.949999809,
        age=48.0,
    )

    # Patient 2: 35-year-old male (gender=1)
    patient2_full = KdmInput(
        albumin=4.5,
        alkaline_phosphatase=74.0,
        log_crp=0.1906203542,
        total_cholesterol=225.0,
        log_creatinine=0.6770178219,
        hba1c=4.599999905,
        systolic_blood_pressure=130.0,
        blood_urea_nitrogen=14.0,
        uric_acid=6.400000095,
        lymphocyte_percent=27.20000076,
        mean_cell_volume=90.40000153,
        white_blood_cell_count=5.900000095,
        age=35.0,
    )

    # Create reduced versions with only PhenoAge biomarkers
    # (excluding: total_cholesterol, hba1c, systolic_blood_pressure, blood_urea_nitrogen, uric_acid)
    patient1_phenoage_only = KdmInput(
        albumin=4.0,
        alkaline_phosphatase=59.0,
        log_crp=0.1906203542,
        total_cholesterol=None,
        log_creatinine=0.4599533006,
        hba1c=None,
        systolic_blood_pressure=None,
        blood_urea_nitrogen=None,
        uric_acid=None,
        lymphocyte_percent=32.34999847,
        mean_cell_volume=92.40000153,
        white_blood_cell_count=4.949999809,
        age=48.0,
    )

    patient2_phenoage_only = KdmInput(
        albumin=4.5,
        alkaline_phosphatase=74.0,
        log_crp=0.1906203542,
        total_cholesterol=None,
        log_creatinine=0.6770178219,
        hba1c=None,
        systolic_blood_pressure=None,
        blood_urea_nitrogen=None,
        uric_acid=None,
        lymphocyte_percent=27.20000076,
        mean_cell_volume=90.40000153,
        white_blood_cell_count=5.900000095,
        age=35.0,
    )

    # Expected KDM values from CSV
    expected_kdm = {"patient1": 47.93003972, "patient2": 35.12392662}

    print("=== KDM Algorithm Manual Testing ===\n")

    # Test Patient 1 with all biomarkers
    print("Patient 1 (48-year-old female) - All biomarkers:")
    chrono_age1, bio_age1, accel_age1 = kdm_age(patient1_full, sex="female")
    print(f"  Chronological Age: {chrono_age1:.2f}")
    print(f"  Biological Age: {bio_age1:.2f}")
    print(f"  Age Acceleration: {accel_age1:.2f}")
    print(f"  Expected KDM: {expected_kdm['patient1']:.2f}")
    print(
        f"  Difference from expected: {abs(bio_age1 - expected_kdm['patient1']):.6f}\n"
    )

    # Test Patient 1 with PhenoAge biomarkers only
    print("Patient 1 (48-year-old female) - PhenoAge biomarkers only:")
    chrono_age1_reduced, bio_age1_reduced, accel_age1_reduced = kdm_age(
        patient1_phenoage_only, sex="female"
    )
    print(f"  Chronological Age: {chrono_age1_reduced:.2f}")
    print(f"  Biological Age: {bio_age1_reduced:.2f}")
    print(f"  Age Acceleration: {accel_age1_reduced:.2f}")
    print(
        f"  Difference from full biomarker set: {abs(bio_age1 - bio_age1_reduced):.2f}\n"
    )

    # Test Patient 2 with all biomarkers
    print("Patient 2 (35-year-old male) - All biomarkers:")
    chrono_age2, bio_age2, accel_age2 = kdm_age(patient2_full, sex="male")
    print(f"  Chronological Age: {chrono_age2:.2f}")
    print(f"  Biological Age: {bio_age2:.2f}")
    print(f"  Age Acceleration: {accel_age2:.2f}")
    print(f"  Expected KDM: {expected_kdm['patient2']:.2f}")
    print(
        f"  Difference from expected: {abs(bio_age2 - expected_kdm['patient2']):.6f}\n"
    )

    # Test Patient 2 with PhenoAge biomarkers only
    print("Patient 2 (35-year-old male) - PhenoAge biomarkers only:")
    chrono_age2_reduced, bio_age2_reduced, accel_age2_reduced = kdm_age(
        patient2_phenoage_only, sex="male"
    )
    print(f"  Chronological Age: {chrono_age2_reduced:.2f}")
    print(f"  Biological Age: {bio_age2_reduced:.2f}")
    print(f"  Age Acceleration: {accel_age2_reduced:.2f}")
    print(
        f"  Difference from full biomarker set: {abs(bio_age2 - bio_age2_reduced):.2f}\n"
    )

    print("=== Summary ===")
    print("KDM can work with different subsets of biomarkers.")
    print("Using all biomarkers provides results very close to expected values.")
    print("Using only PhenoAge biomarkers still produces reasonable results.")
