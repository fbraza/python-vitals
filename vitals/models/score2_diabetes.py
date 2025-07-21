"""
Module for computing the SCORE2-Diabetes cardiovascular risk assessment.

This module implements the SCORE2-Diabetes algorithm for 10-year cardiovascular disease
risk estimation in patients with diabetes.
"""

import math
from pathlib import Path

import numpy as np

from vitals.biomarkers import exceptions, helpers
from vitals.schemas.score2 import (
    BaselineSurvival,
    CalibrationScales,
    FemaleCoefficientsDiabeticModel,
    MaleCoefficientsDiabeticModel,
    MarkersDiabetes,
    UnitsDiabetes,
)


def compute(
    filepath: str | Path,
) -> tuple[float, float, helpers.RiskCategory] | None:
    """
    Calculate the 10-year cardiovascular disease risk using the SCORE2-Diabetes algorithm.

    This function implements the SCORE2-Diabetes risk assessment for patients with diabetes.
    It uses sex-specific Cox proportional hazards model coefficients and applies regional
    calibration for Belgium (Low Risk region).

    Args:
        filepath: Path to JSON file containing biomarker data including age, sex,
                 systolic blood pressure, total cholesterol, HDL cholesterol, smoking status,
                 diabetes status, age at diabetes diagnosis, HbA1c, and eGFR.

    Returns:
        A tuple containing:
        - age: The patient's chronological age
        - risk_percentage: The calibrated 10-year CVD risk as a percentage
        - risk_category: Risk stratification category ("Low to moderate", "High", or "Very high")

    Raises:
        ValueError: If invalid biomarker class is used
    """
    # Extract biomarkers from JSON file
    try:
        biomarkers = helpers.extract_biomarkers_from_json(
            filepath=filepath,
            biomarker_class=MarkersDiabetes,
            biomarker_units=UnitsDiabetes(),
        )
    except exceptions.BiomarkerNotFound:
        return None

    age: float = biomarkers.age
    is_male: bool = biomarkers.is_male  # True for male, False for female

    # Apply transformations to biomarkers
    cage: float = (age - 60) / 5
    smoking: float = float(biomarkers.smoking)  # Convert bool to float (1.0 or 0.0)
    csbp: float = (biomarkers.systolic_blood_pressure - 120) / 20
    diabetes: float = float(biomarkers.diabetes)  # Convert bool to float (1.0 or 0.0)
    ctchol: float = biomarkers.total_cholesterol - 6
    chdl: float = (biomarkers.hdl_cholesterol - 1.3) / 0.5
    cagediab: float = diabetes * (biomarkers.age_at_diabetes_diagnosis - 50) / 5
    ca1c: float = (biomarkers.hba1c - 31) / 9.34
    cegfr: float = (math.log(biomarkers.egfr) - 4.5) / 0.15
    cegfr_squared: float = cegfr * cegfr

    # Calculate interaction terms
    smoking_age: float = smoking * cage
    sbp_age: float = csbp * cage
    diabetes_age: float = diabetes * cage
    tchol_age: float = ctchol * cage
    hdl_age: float = chdl * cage
    hba1c_age: float = ca1c * cage
    egfr_age: float = cegfr * cage

    # Get sex-specific coefficients and calibration values
    baseline_survival_model = BaselineSurvival()
    calibration_scales = CalibrationScales()

    coef: MaleCoefficientsDiabeticModel | FemaleCoefficientsDiabeticModel
    if is_male:
        coef = MaleCoefficientsDiabeticModel()
        baseline_survival = baseline_survival_model.male
        scale1 = calibration_scales.male_scale1
        scale2 = calibration_scales.male_scale2
    else:
        coef = FemaleCoefficientsDiabeticModel()
        baseline_survival = baseline_survival_model.female
        scale1 = calibration_scales.female_scale1
        scale2 = calibration_scales.female_scale2

    linear_pred = (
        coef.age * cage
        + coef.smoking * smoking
        + coef.sbp * csbp
        + coef.diabetes * diabetes
        + coef.total_cholesterol * ctchol
        + coef.hdl_cholesterol * chdl
        + coef.age_at_diabetes_diagnosis * cagediab
        + coef.hba1c * ca1c
        + coef.egfr * cegfr
        + coef.egfr_squared * cegfr_squared
        + coef.smoking_age * smoking_age
        + coef.sbp_age * sbp_age
        + coef.diabetes_age * diabetes_age
        + coef.tchol_age * tchol_age
        + coef.hdl_age * hdl_age
        + coef.hba1c_age * hba1c_age
        + coef.egfr_age * egfr_age
    )

    # Calculate uncalibrated risk
    uncalibrated_risk: float = 1 - np.power(baseline_survival, np.exp(linear_pred))

    # Apply calibration for Belgium (Low Risk region)
    calibrated_risk: float = helpers.apply_calibration(
        uncalibrated_risk, scale1, scale2
    )

    # Determine risk category based on age
    risk_category: helpers.RiskCategory = helpers.determine_risk_category(
        age, calibrated_risk
    )

    return (age, round(calibrated_risk, 2), risk_category)
