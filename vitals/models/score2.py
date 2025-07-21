"""
Module for computing the SCORE2 cardiovascular risk assessment.

This module implements the SCORE2 algorithm for 10-year cardiovascular disease risk estimation
in apparently healthy individuals aged 40-69 years in Europe.
"""

from pathlib import Path

import numpy as np

from vitals.biomarkers import helpers
from vitals.schemas.score2 import (
    BaselineSurvival,
    CalibrationScales,
    FemaleCoefficientsBaseModel,
    MaleCoefficientsBaseModel,
    Markers,
    Units,
)


def compute(
    filepath: str | Path,
) -> tuple[float, float, helpers.RiskCategory] | None:
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
    # Validate biomarkers are available for SCORE2 algorithm
    biomarkers = helpers.validate_biomarkers_for_algorithm(
        filepath=filepath,
        biomarker_class=Markers,
        biomarker_units=Units(),
    )
    if biomarkers is None:
        return None

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

    coef: MaleCoefficientsBaseModel | FemaleCoefficientsBaseModel
    if is_male:
        coef = MaleCoefficientsBaseModel()
        baseline_survival = baseline_survival_model.male
        scale1 = calibration_scales.male_scale1
        scale2 = calibration_scales.male_scale2
    else:
        coef = FemaleCoefficientsBaseModel()
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
    calibrated_risk: float = helpers.apply_calibration(
        uncalibrated_risk, scale1, scale2
    )

    # Determine risk category based on age
    risk_category: helpers.RiskCategory = helpers.determine_risk_category(
        age, calibrated_risk
    )

    return (age, round(calibrated_risk, 2), risk_category)
