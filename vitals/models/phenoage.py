from pathlib import Path

import numpy as np

from vitals.biomarkers import exceptions, helpers
from vitals.schemas.phenoage import Gompertz, LinearModel, Markers, Units


def compute(filepath: str | Path) -> tuple[float, float, float] | None:
    """
    The Phenoage score is calculated as a weighted (coefficients available in Levine et al 2018)
    linear combination of these variables, which was then transformed into units of years using 2 parametric
    (Gompertz distribution) proportional hazard models—one for the linearly combined score for all 10 variables
    and another for chronological age. Thus, PhenoAge represents the expected age within the population that
    corresponds to a person’s estimated hazard of mortality as a function of his/her biological profile.
    """
    # Extract biomarkers from JSON file
    try:
        biomarkers = helpers.extract_biomarkers_from_json(
            filepath=filepath,
            biomarker_class=Markers,
            biomarker_units=Units(),
        )
    except exceptions.BiomarkerNotFound:
        return None

    age: float = biomarkers.age
    coef: LinearModel = LinearModel()

    # if isinstance(biomarkers, Markers):
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
    gompertz = helpers.gompertz_mortality_model(weighted_risk_score=weighted_risk_score)
    model = Gompertz()
    pred_age = model.coef1 + np.log(model.coef2 * np.log(1 - gompertz)) / model.coef3
    accl_age = pred_age - age
    return (age, pred_age, accl_age)
    # else:
    #     raise ValueError(f"Invalid biomarker class used: {biomarkers}")
