"""
Module for computing the SCORE2 cardiovascular risk assessment.

This module implements the SCORE2 algorithm for 10-year cardiovascular disease risk estimation
in apparently healthy individuals aged 40-69 years in Europe.
"""

from pathlib import Path
from typing import Literal, TypeAlias

import numpy as np
from pydantic import BaseModel

from vitals.biomarkers import helpers, schemas

RiskCategory: TypeAlias = Literal["Low to moderate", "High", "Very high"]


class ModelCoefficients(BaseModel):
    """
    Sex-specific coefficients for the SCORE2 Cox proportional hazards model.

    These coefficients are used to calculate the 10-year risk of cardiovascular disease
    based on transformed risk factors and their age interactions.
    """

    # Male coefficients
    male_age: float = 0.3742
    male_smoking: float = 0.6012
    male_sbp: float = 0.2777
    male_total_cholesterol: float = 0.1458
    male_hdl_cholesterol: float = -0.2698

    # Male interaction term coefficients
    male_smoking_age: float = -0.0755
    male_sbp_age: float = -0.0255
    male_tchol_age: float = -0.0281
    male_hdl_age: float = 0.0426

    # Female coefficients
    female_age: float = 0.4648
    female_smoking: float = 0.7744
    female_sbp: float = 0.3131
    female_total_cholesterol: float = 0.1002
    female_hdl_cholesterol: float = -0.2606

    # Female interaction term coefficients
    female_smoking_age: float = -0.1088
    female_sbp_age: float = -0.0277
    female_tchol_age: float = -0.0226
    female_hdl_age: float = 0.0613


class BaselineSurvival(BaseModel):
    """
    Sex-specific baseline survival probabilities for the SCORE2 model.

    These values represent the 10-year survival probability for individuals
    with all risk factors at their reference values.
    """

    male: float = 0.9605
    female: float = 0.9776


class CalibrationScales(BaseModel):
    """
    Region and sex-specific calibration scales for Belgium (Low Risk region).

    These scales are used to calibrate the uncalibrated risk estimate to match
    the population-specific cardiovascular disease incidence rates.
    """

    # Male calibration scales
    male_scale1: float = -0.5699
    male_scale2: float = 0.7476

    # Female calibration scales
    female_scale1: float = -0.7380
    female_scale2: float = 0.7019


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
        biomarker_class=schemas.Score2Markers,
        biomarker_units=schemas.Score2Units(),
    )

    if not isinstance(biomarkers, schemas.Score2Markers):
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

    # Get model coefficients
    coef: ModelCoefficients = ModelCoefficients()

    # Calculate linear predictor (x) based on sex

    linear_pred: float
    baseline_survival: float
    scale1: float
    scale2: float

    if is_male:
        linear_pred = (
            coef.male_age * cage
            + coef.male_smoking * smoking
            + coef.male_sbp * csbp
            + coef.male_total_cholesterol * ctchol
            + coef.male_hdl_cholesterol * chdl
            + coef.male_smoking_age * smoking_age
            + coef.male_sbp_age * sbp_age
            + coef.male_tchol_age * tchol_age
            + coef.male_hdl_age * hdl_age
        )
        baseline_survival = BaselineSurvival().male
        scale1 = CalibrationScales().male_scale1
        scale2 = CalibrationScales().male_scale2
    else:
        linear_pred = (
            coef.female_age * cage
            + coef.female_smoking * smoking
            + coef.female_sbp * csbp
            + coef.female_total_cholesterol * ctchol
            + coef.female_hdl_cholesterol * chdl
            + coef.female_smoking_age * smoking_age
            + coef.female_sbp_age * sbp_age
            + coef.female_tchol_age * tchol_age
            + coef.female_hdl_age * hdl_age
        )
        baseline_survival = BaselineSurvival().female
        scale1 = CalibrationScales().female_scale1
        scale2 = CalibrationScales().female_scale2

    # Calculate uncalibrated risk
    uncalibrated_risk: float = 1 - np.power(baseline_survival, np.exp(linear_pred))

    # Apply calibration for Belgium (Low Risk region)
    # Calibrated 10-year risk, % = [1 - exp(-exp(scale1 + scale2*ln(-ln(1 - 10-year risk))))] * 100
    calibrated_risk: float = float(
        (1 - np.exp(-np.exp(scale1 + scale2 * np.log(-np.log(1 - uncalibrated_risk)))))
        * 100
    )

    # Determine risk category based on age
    risk_category: RiskCategory
    if age < 50:
        if calibrated_risk < 2.5:
            risk_category = "Low to moderate"
        elif calibrated_risk < 7.5:
            risk_category = "High"
        else:
            risk_category = "Very high"
    else:  # age 50-69
        if calibrated_risk < 5:
            risk_category = "Low to moderate"
        elif calibrated_risk < 10:
            risk_category = "High"
        else:
            risk_category = "Very high"

    return (age, round(calibrated_risk, 2), risk_category)
