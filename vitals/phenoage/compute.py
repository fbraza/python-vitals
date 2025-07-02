import json

import levine_params as levine
import numpy as np
from pydantic import BaseModel


class PhenoAgeMarkers(BaseModel):
    """Processed PhenoAge biomarkers with standardized units."""

    albumin: float
    creatinine: float
    glucose: float
    crp: float
    lymphocyte_percent: float
    mean_cell_volume: float
    red_cell_distribution_width: float
    alkaline_phosphatase: float
    white_blood_cell_count: float
    age: float


def extract_biomarkers_from_json(filepath: str) -> PhenoAgeMarkers:
    """
    Extract required biomarkers from JSON file based on expected names and units.

    Args:
        filepath: Path to JSON file containing biomarker data

    Returns:
        PhenoAgeMarkers instance with extracted values
    """
    with open(filepath) as f:
        data = json.load(f)

    raw_biomarkers = data.get("raw_biomarkers", {})
    expected_units = levine.Unit()
    expected_units_dict = expected_units.model_dump()

    # Get required biomarker field names from PhenoAgeMarkers
    required_fields = PhenoAgeMarkers.model_fields.keys()
    extracted_values = {}

    for field_name in required_fields:
        expected_unit = expected_units_dict[field_name]

        value = _find_biomarker_value(raw_biomarkers, field_name, expected_unit)
        if value is None:
            raise ValueError(
                f"Could not find {field_name} biomarker with unit {expected_unit}"
            )
        extracted_values[field_name] = value

    return PhenoAgeMarkers(**extracted_values)


def _find_biomarker_value(
    raw_biomarkers: dict, biomarker_name: str, expected_unit: str
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


def gompertz_mortality_model(weighted_risk_score: float) -> float:
    __params = levine.Gompertz()
    return 1 - np.exp(
        -np.exp(weighted_risk_score)
        * (np.exp(120 * __params.lambda_) - 1)
        / __params.lambda_
    )


def phenoage(filepath: str) -> tuple[float, float, float]:
    """
    The Phenoage score is calculated as a weighted (coefficients available in Levine et al 2018)
    linear combination of these variables, which was then transformed into units of years using 2 parametric
    (Gompertz distribution) proportional hazard models—one for the linearly combined score for all 10 variables
    and another for chronological age. Thus, PhenoAge represents the expected age within the population that
    corresponds to a person’s estimated hazard of mortality as a function of his/her biological profile.
    """
    # Extract biomarkers from JSON file
    biomarkers = extract_biomarkers_from_json(filepath)

    age = biomarkers.age
    coef = levine.LinearModel()
    weighted_risk_score = (
        coef.intercept
        + (coef.albumin * biomarkers.albumin)
        + (coef.creatinine * biomarkers.creatinine)
        + (coef.glucose * biomarkers.glucose)
        + (coef.log_crp * np.log(biomarkers.crp))
        + (coef.lymphocyte_percent * biomarkers.lymphocyte_percent)
        + (coef.mean_cell_volume * biomarkers.mean_cell_volume)
        + (coef.red_cell_distribution_width * biomarkers.red_cell_distribution_width)
        + (coef.alkaline_phosphatase * biomarkers.alkaline_phosphatase)
        + (coef.white_blood_cell_count * biomarkers.white_blood_cell_count)
        + (coef.age * biomarkers.age)
    )

    gompertz = gompertz_mortality_model(weighted_risk_score=weighted_risk_score)
    model = levine.Gompertz()
    pred_age = model.coef1 + np.log(model.coef2 * np.log(1 - gompertz)) / model.coef3
    accl_age = pred_age - age
    return (age, pred_age, accl_age)


if __name__ == "__main__":
    age, pred_age, accl_age = phenoage(
        "/Users/fbraza/Documents/python_phenoage/tests/outputs/test__input__patient_01.json"
    )
    print(f"Age: {age:.2f} years")
    print(f"Predicted Age: {pred_age:.2f} years")
    print(f"Accelerated Age: {accl_age:.2f} years")
