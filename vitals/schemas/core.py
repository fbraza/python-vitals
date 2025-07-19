from typing import Literal, TypeAlias

import numpy as np
from pydantic import BaseModel

RiskCategory: TypeAlias = Literal["Low to moderate", "High", "Very high"]


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


def determine_risk_category(age: float, calibrated_risk: float) -> RiskCategory:
    """
    Determine cardiovascular risk category based on age and calibrated risk percentage.

    Args:
        age: Patient's age in years
        calibrated_risk: Calibrated 10-year CVD risk as a percentage

    Returns:
        Risk stratification category
    """
    if age < 50:
        if calibrated_risk < 2.5:
            return "Low to moderate"
        elif calibrated_risk < 7.5:
            return "High"
        else:
            return "Very high"
    else:  # age 50-69
        if calibrated_risk < 5:
            return "Low to moderate"
        elif calibrated_risk < 10:
            return "High"
        else:
            return "Very high"


def apply_calibration(uncalibrated_risk: float, scale1: float, scale2: float) -> float:
    """
    Apply regional calibration to uncalibrated risk estimate.

    Args:
        uncalibrated_risk: Raw risk estimate from the Cox model
        scale1: First calibration scale parameter
        scale2: Second calibration scale parameter

    Returns:
        Calibrated 10-year CVD risk as a percentage
    """
    return float(
        (1 - np.exp(-np.exp(scale1 + scale2 * np.log(-np.log(1 - uncalibrated_risk)))))
        * 100
    )
