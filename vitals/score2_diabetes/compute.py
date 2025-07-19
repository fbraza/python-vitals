"""
Module for computing the SCORE2-Diabetes cardiovascular risk assessment.

This module implements the SCORE2-Diabetes algorithm for 10-year cardiovascular disease
risk estimation in patients with diabetes.
"""

import math
from pathlib import Path

import numpy as np

from vitals.biomarkers import helpers
from vitals.schemas.coefficients import (
    Score2DiabetesFemaleCoefficients,
    Score2DiabetesMaleCoefficients,
)
from vitals.schemas.core import (
    BaselineSurvival,
    CalibrationScales,
    RiskCategory,
    apply_calibration,
    determine_risk_category,
)
from vitals.schemas.markers import Score2DiabetesMarkers
from vitals.schemas.units import Score2DiabetesUnits


def cardiovascular_risk(filepath: str | Path) -> tuple[float, float, RiskCategory]:
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
    biomarkers = helpers.extract_biomarkers_from_json(
        filepath=filepath,
        biomarker_class=Score2DiabetesMarkers,
        biomarker_units=Score2DiabetesUnits(),
    )

    if not isinstance(biomarkers, Score2DiabetesMarkers):
        raise ValueError(f"Invalid biomarker class used: {biomarkers}")

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

    if is_male:
        male_coef = Score2DiabetesMaleCoefficients()
        linear_pred = (
            male_coef.age * cage
            + male_coef.smoking * smoking
            + male_coef.sbp * csbp
            + male_coef.diabetes * diabetes
            + male_coef.total_cholesterol * ctchol
            + male_coef.hdl_cholesterol * chdl
            + male_coef.age_at_diabetes_diagnosis * cagediab
            + male_coef.hba1c * ca1c
            + male_coef.egfr * cegfr
            + male_coef.egfr_squared * cegfr_squared
            + male_coef.smoking_age * smoking_age
            + male_coef.sbp_age * sbp_age
            + male_coef.diabetes_age * diabetes_age
            + male_coef.tchol_age * tchol_age
            + male_coef.hdl_age * hdl_age
            + male_coef.hba1c_age * hba1c_age
            + male_coef.egfr_age * egfr_age
        )
        baseline_survival = baseline_survival_model.male
        scale1 = calibration_scales.male_scale1
        scale2 = calibration_scales.male_scale2
    else:
        female_coef = Score2DiabetesFemaleCoefficients()
        linear_pred = (
            female_coef.age * cage
            + female_coef.smoking * smoking
            + female_coef.sbp * csbp
            + female_coef.diabetes * diabetes
            + female_coef.total_cholesterol * ctchol
            + female_coef.hdl_cholesterol * chdl
            + female_coef.age_at_diabetes_diagnosis * cagediab
            + female_coef.hba1c * ca1c
            + female_coef.egfr * cegfr
            + female_coef.egfr_squared * cegfr_squared
            + female_coef.smoking_age * smoking_age
            + female_coef.sbp_age * sbp_age
            + female_coef.diabetes_age * diabetes_age
            + female_coef.tchol_age * tchol_age
            + female_coef.hdl_age * hdl_age
            + female_coef.hba1c_age * hba1c_age
            + female_coef.egfr_age * egfr_age
        )
        baseline_survival = baseline_survival_model.female
        scale1 = calibration_scales.female_scale1
        scale2 = calibration_scales.female_scale2

    # Calculate uncalibrated risk
    uncalibrated_risk: float = 1 - np.power(baseline_survival, np.exp(linear_pred))

    # Apply calibration for Belgium (Low Risk region)
    calibrated_risk: float = apply_calibration(uncalibrated_risk, scale1, scale2)

    # Determine risk category based on age
    risk_category: RiskCategory = determine_risk_category(age, calibrated_risk)

    return (age, round(calibrated_risk, 2), risk_category)
