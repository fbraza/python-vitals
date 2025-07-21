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


def format_unit_suffix(unit: str) -> str:
    """Convert unit string to a valid suffix format.

    Args:
        unit: Unit string (e.g., "mg/dL", "1000 cells/uL")

    Returns:
        Formatted suffix (e.g., "mg_dl", "1000_cells_ul")
    """
    # Replace special characters with underscores
    suffix = unit.lower()
    suffix = suffix.replace("/", "_")
    suffix = suffix.replace(" ", "_")
    suffix = suffix.replace("^", "")
    return suffix


def update_biomarker_names(biomarkers: dict[str, Any]) -> dict[str, Any]:
    """Update biomarker names to include unit suffixes.

    Args:
        biomarkers: Dictionary of biomarker data with value and unit

    Returns:
        Updated dictionary with unit-suffixed biomarker names
    """
    updated_biomarkers = {}

    for name, data in biomarkers.items():
        if isinstance(data, dict) and "unit" in data:
            unit_suffix = format_unit_suffix(data["unit"])
            new_name = f"{name}_{unit_suffix}"
            updated_biomarkers[new_name] = data
        else:
            # Keep as is if not in expected format
            updated_biomarkers[name] = data

    return updated_biomarkers


def find_biomarker_value(
    raw_biomarkers: dict[str, Any], biomarker_name: str, expected_unit: str
) -> float | None:
    """
    Find biomarker value by name prefix and expected unit.

    Args:
        raw_biomarkers: Dictionary of biomarker data
        biomarker_name: Name of biomarker to find (without unit suffix)
        expected_unit: Expected unit for this biomarker

    Returns:
        Biomarker value if found, None otherwise
    """
    for key, biomarker_data in raw_biomarkers.items():
        if key.startswith(biomarker_name) and isinstance(biomarker_data, dict):
            unit = biomarker_data.get("unit", "")
            if unit == expected_unit:
                return biomarker_data.get("value")

    return None


def add_converted_biomarkers(biomarkers: dict[str, Any]) -> dict[str, Any]:
    """Add converted biomarker entries for glucose, creatinine, albumin, and CRP.

    Args:
        biomarkers: Dictionary of biomarkers with unit-suffixed names

    Returns:
        Dictionary with original and converted biomarkers
    """
    # Copy original biomarkers
    result = biomarkers.copy()

    # Conversion mappings
    conversions: dict[str, ConversionInfo] = {
        "glucose_mg_dl": {
            "target_name": "glucose_mmol_l",
            "target_unit": "mmol/L",
            "conversion": lambda x: x / 18.0,
        },
        "glucose_mmol_l": {
            "target_name": "glucose_mg_dl",
            "target_unit": "mg/dL",
            "conversion": lambda x: x * 18.0,
        },
        "creatinine_mg_dl": {
            "target_name": "creatinine_umol_l",
            "target_unit": "umol/L",
            "conversion": lambda x: x * 88.4,
        },
        "creatinine_umol_l": {
            "target_name": "creatinine_mg_dl",
            "target_unit": "mg/dL",
            "conversion": lambda x: x / 88.4,
        },
        "albumin_g_dl": {
            "target_name": "albumin_g_l",
            "target_unit": "g/L",
            "conversion": lambda x: x * 10.0,
        },
        "albumin_g_l": {
            "target_name": "albumin_g_dl",
            "target_unit": "g/dL",
            "conversion": lambda x: x / 10.0,
        },
        "crp_mg_l": {
            "target_name": "crp_mg_dl",
            "target_unit": "mg/dL",
            "conversion": lambda x: x / 10.0,
        },
        "crp_mg_dl": {
            "target_name": "crp_mg_l",
            "target_unit": "mg/L",
            "conversion": lambda x: x * 10.0,
        },
    }

    # Add converted entries
    for source_name, conversion_info in conversions.items():
        if source_name in biomarkers:
            source_value = biomarkers[source_name]["value"]
            target_name = conversion_info["target_name"]

            # Skip if target already exists
            if target_name not in result:
                converted_value = conversion_info["conversion"](source_value)
                result[target_name] = {
                    "value": round(converted_value, 4),
                    "unit": conversion_info["target_unit"],
                }

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
        model_class: Pydantic model class defining required biomarkers
        units_model: Pydantic model instance containing expected units

    Returns:
        Instance of model_class with extracted biomarker values

    Raises:
        ValueError: If required biomarker is not found with expected unit
    """
    with open(filepath) as f:
        data = json.load(f)

    raw_biomarkers = data.get("raw_biomarkers", {})
    expected_units_dict = biomarker_units.model_dump()

    # Get required biomarker field names from model
    required_fields = biomarker_class.model_fields
    extracted_values = {}

    for field_name in required_fields:
        expected_unit = expected_units_dict.get(field_name)
        if expected_unit is None:
            raise ValueError(f"No expected unit defined for {field_name}")

        value: int | float | None = find_biomarker_value(
            raw_biomarkers, field_name, expected_unit
        )
        if value is None:
            raise BiomarkerNotFound(
                f"Biomarker '{field_name}' not found : Stop computation"
            )
        extracted_values[field_name] = value

    return biomarker_class(**extracted_values)


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
