from pathlib import Path

import numpy as np
from pydantic import BaseModel

from vitals.biomarkers import helpers, schemas


class LinearModel(BaseModel):
    """
    Coefficients used to calculate the PhenoAge from Levine et al 2018
    """

    intercept: float = -19.9067
    albumin: float = -0.0336
    creatinine: float = 0.0095
    glucose: float = 0.1953
    log_crp: float = 0.0954
    lymphocyte_percent: float = -0.0120
    mean_cell_volume: float = 0.0268
    red_cell_distribution_width: float = 0.3306
    alkaline_phosphatase: float = 0.00188
    white_blood_cell_count: float = 0.0554
    age: float = 0.0804


class Gompertz(BaseModel):
    """
    Parameters of the Gompertz distribution for PhenoAge computation
    """

    lambda_: float = 0.0192
    coef1: float = 141.50225
    coef2: float = -0.00553
    coef3: float = 0.090165


def __gompertz_mortality_model(weighted_risk_score: float) -> float:
    __params = Gompertz()
    return 1 - np.exp(
        -np.exp(weighted_risk_score)
        * (np.exp(120 * __params.lambda_) - 1)
        / __params.lambda_
    )


def biological_age(filepath: str | Path) -> tuple[float, float, float]:
    """
    The Phenoage score is calculated as a weighted (coefficients available in Levine et al 2018)
    linear combination of these variables, which was then transformed into units of years using 2 parametric
    (Gompertz distribution) proportional hazard models—one for the linearly combined score for all 10 variables
    and another for chronological age. Thus, PhenoAge represents the expected age within the population that
    corresponds to a person’s estimated hazard of mortality as a function of his/her biological profile.
    """
    # Extract biomarkers from JSON file
    biomarkers = helpers.extract_biomarkers_from_json(
        filepath=filepath,
        biomarker_class=schemas.PhenoageMarkers,
        biomarker_units=schemas.PhenoageUnits(),
    )

    age = biomarkers.age
    coef = LinearModel()

    if isinstance(biomarkers, schemas.PhenoageMarkers):
        weighted_risk_score = (
            coef.intercept
            + (coef.albumin * biomarkers.albumin)
            + (coef.creatinine * biomarkers.creatinine)
            + (coef.glucose * biomarkers.glucose)
            + (coef.log_crp * np.log(biomarkers.crp))
            + (coef.lymphocyte_percent * biomarkers.lymphocyte_percent)
            + (coef.mean_cell_volume * biomarkers.mean_cell_volume)
            + (
                coef.red_cell_distribution_width
                * biomarkers.red_cell_distribution_width
            )
            + (coef.alkaline_phosphatase * biomarkers.alkaline_phosphatase)
            + (coef.white_blood_cell_count * biomarkers.white_blood_cell_count)
            + (coef.age * biomarkers.age)
        )
        gompertz = __gompertz_mortality_model(weighted_risk_score=weighted_risk_score)
        model = Gompertz()
        pred_age = (
            model.coef1 + np.log(model.coef2 * np.log(1 - gompertz)) / model.coef3
        )
        accl_age = pred_age - age
        return (age, pred_age, accl_age)
    else:
        raise ValueError(f"Invalid biomarker class used: {biomarkers}")


# if __name__ == "__main__":
#     from pathlib import Path
#     input_dir = Path("tests/outputs")
#     output_dir = Path("tests/outputs")

#     for input_file in input_dir.glob("*.json"):
#         if "patient" not in str(input_file):
#             continue

#         # Update biomarker data
#         age, pred_age, accl_age = biological_age(str(input_file))
#         print(f"Chrono Age: {age} ::: Predicted Age: {pred_age} ::: Accel {accl_age}")
