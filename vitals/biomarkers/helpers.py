import json
from collections.abc import Callable
from pathlib import Path
from typing import Any, Literal, TypeAlias, TypedDict, TypeVar

import numpy as np
from pydantic import BaseModel

from vitals.biomarkers.exceptions import BiomarkerNotFound
from vitals.schemas import phenoage, score2

RiskCategory: TypeAlias = Literal["Low to moderate", "High", "Very high"]
Biomarkers = TypeVar("Biomarkers", bound=BaseModel)
Units = phenoage.Units | score2.Units | score2.UnitsDiabetes


class ConversionInfo(TypedDict):
    """Type definition for biomarker conversion information."""

    target_name: str
    target_unit: str
    conversion: Callable[[float], float]


def add_converted_biomarkers(biomarkers: dict[str, Any]) -> dict[str, Any]:
    """Add converted biomarker entries for glucose, creatinine, albumin, and CRP.

    Args:
        biomarkers: Dictionary of biomarkers with unit-keyed values

    Returns:
        Dictionary with original and converted biomarkers
    """
    # Deep copy to avoid modifying original
    result = {k: v.copy() for k, v in biomarkers.items()}

    # Conversion mappings: biomarker -> [(source_unit, target_unit, conversion_func)]
    conversions: dict[str, list[tuple[str, str, Callable]]] = {
        "glucose": [
            ("mg/dL", "mmol/L", lambda x: x / 18.0),
            ("mmol/L", "mg/dL", lambda x: x * 18.0),
        ],
        "creatinine": [
            ("mg/dL", "umol/L", lambda x: x * 88.4),
            ("umol/L", "mg/dL", lambda x: x / 88.4),
        ],
        "albumin": [
            ("g/dL", "g/L", lambda x: x * 10.0),
            ("g/L", "g/dL", lambda x: x / 10.0),
        ],
        "crp": [
            ("mg/L", "mg/dL", lambda x: x / 10.0),
            ("mg/dL", "mg/L", lambda x: x * 10.0),
        ],
    }

    # Add converted entries
    for biomarker_name, conversion_list in conversions.items():
        if biomarker_name in result:
            for source_unit, target_unit, conversion_func in conversion_list:
                if (
                    source_unit in result[biomarker_name]
                    and target_unit not in result[biomarker_name]
                ):
                    source_value = result[biomarker_name][source_unit]
                    converted_value = round(conversion_func(source_value), 4)
                    result[biomarker_name][target_unit] = converted_value

    return result


def extract_biomarkers_from_json(
    filepath: str | Path,
    biomarker_class: type[Biomarkers],
    biomarker_units: Units,
) -> Biomarkers:
    """
    Generic function to extract biomarkers from JSON file based on a Pydantic model.

    Args:
        filepath: Path to JSON file containing biomarker data
        biomarker_class: Pydantic model class defining required biomarkers
        biomarker_units: Pydantic model instance containing expected units

    Returns:
        Instance of biomarker_class with extracted biomarker values

    Raises:
        BiomarkerNotFound: If required biomarker is not found with expected unit
    """
    with open(filepath) as f:
        data = json.load(f)

    raw_biomarkers = data.get("raw_biomarkers", {})
    expected_units_dict = biomarker_units.model_dump()
    required_fields = biomarker_class.model_fields

    # Build biomarkers dictionary using comprehension
    biomarkers_for_scoring = {
        field: raw_biomarkers.get(field, {}).get(expected_units_dict[field])
        for field in required_fields
    }

    # Check for missing biomarkers and raise appropriate errors
    for field, value in biomarkers_for_scoring.items():
        if value is None:
            raise BiomarkerNotFound(f"Biomarker '{field}' not found : Stop computation")

    return biomarker_class(**biomarkers_for_scoring)


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


def gompertz_mortality_model(weighted_risk_score: float) -> float:
    params = phenoage.Gompertz()
    return 1 - np.exp(
        -np.exp(weighted_risk_score)
        * (np.exp(120 * params.lambda_) - 1)
        / params.lambda_
    )
