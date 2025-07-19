"""
Module for computing the SCORE2 cardiovascular risk assessment.

This module implements the SCORE2 algorithm for 10-year cardiovascular disease risk estimation
in apparently healthy individuals aged 40-69 years in Europe.
"""

from pathlib import Path

import numpy as np

from vitals.biomarkers import helpers
from vitals.schemas.coefficients import Score2FemaleCoefficients, Score2MaleCoefficients
from vitals.schemas.core import (
    BaselineSurvival,
    CalibrationScales,
    RiskCategory,
    apply_calibration,
    determine_risk_category,
)
from vitals.schemas.markers import Score2Markers
from vitals.schemas.units import Score2Units


def cardiovascular_risk(filepath: str | Path) -> tuple[float, float, RiskCategory]:
    """
    Calculate the 10-year cardiovascular disease risk using the SCORE2 algorithm.

    This function implements the SCORE2 risk assessment for apparently healthy individuals
    aged 40-69 years in Europe. It uses sex-specific Cox proportional hazards model
    coefficients and applies regional calibration for Belgium (Low Risk region).

    Args:
        filepath: Path to JSON file containing biomarker data including age, sex,
                 systolic blood pressure, total cholesterol, HDL cholesterol, and smoking status.

    Returns:
        A tuple containing:
        - age: The patient's chronological age
        - risk_percentage: The calibrated 10-year CVD risk as a percentage
        - risk_category: Risk stratification category ("Low to moderate", "High", or "Very high")

    Raises:
        ValueError: If invalid biomarker class is used
    """
    # Extract biomarkers from JSON file
    biomarkers = helpers.extract_biomarkers_from_json(
        filepath=filepath,
        biomarker_class=Score2Markers,
        biomarker_units=Score2Units(),
    )

    if not isinstance(biomarkers, Score2Markers):
        raise ValueError(f"Invalid biomarker class used: {biomarkers}")

    age: float = biomarkers.age
    is_male: bool = biomarkers.is_male  # True for male, False for female

    # Apply transformations to biomarkers
    cage: float = (age - 60) / 5
    smoking: float = float(biomarkers.smoking)  # Convert bool to float (1.0 or 0.0)
    csbp: float = (biomarkers.systolic_blood_pressure - 120) / 20
    ctchol: float = biomarkers.total_cholesterol - 6
    chdl: float = (biomarkers.hdl_cholesterol - 1.3) / 0.5

    # Calculate interaction terms
    smoking_age: float = smoking * cage
    sbp_age: float = csbp * cage
    tchol_age: float = ctchol * cage
    hdl_age: float = chdl * cage

    # Get sex-specific coefficients and calibration values
    baseline_survival_model = BaselineSurvival()
    calibration_scales = CalibrationScales()

    coef: Score2MaleCoefficients | Score2FemaleCoefficients
    if is_male:
        coef = Score2MaleCoefficients()
        baseline_survival = baseline_survival_model.male
        scale1 = calibration_scales.male_scale1
        scale2 = calibration_scales.male_scale2
    else:
        coef = Score2FemaleCoefficients()
        baseline_survival = baseline_survival_model.female
        scale1 = calibration_scales.female_scale1
        scale2 = calibration_scales.female_scale2

    linear_pred = (
        coef.age * cage
        + coef.smoking * smoking
        + coef.sbp * csbp
        + coef.total_cholesterol * ctchol
        + coef.hdl_cholesterol * chdl
        + coef.smoking_age * smoking_age
        + coef.sbp_age * sbp_age
        + coef.tchol_age * tchol_age
        + coef.hdl_age * hdl_age
    )

    # Calculate uncalibrated risk
    uncalibrated_risk: float = 1 - np.power(baseline_survival, np.exp(linear_pred))

    # Apply calibration for Belgium (Low Risk region)
    calibrated_risk: float = apply_calibration(uncalibrated_risk, scale1, scale2)

    # Determine risk category based on age
    risk_category: RiskCategory = determine_risk_category(age, calibrated_risk)

    return (age, round(calibrated_risk, 2), risk_category)
