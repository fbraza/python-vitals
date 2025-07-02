from typing import TypeAlias

import levine_params as levine
import numpy as np
import utils
from pydantic import BaseModel

Biomarker: TypeAlias = tuple[float, str]


class PhenoAgeInput(BaseModel):
    albumin: Biomarker
    creatinine: Biomarker
    glucose: Biomarker
    log_crp: Biomarker
    lymphocyte_percent: Biomarker
    mean_cell_volume: Biomarker
    red_cell_distribution_width: Biomarker
    alkaline_phosphatase: Biomarker
    white_blood_cell_count: Biomarker
    age: Biomarker


def convert_to_expected_units(
    data: PhenoAgeInput, expected_units: utils.Unit
) -> PhenoAgeInput:
    data_dict = data.model_dump()
    expected_dict = expected_units.model_dump()
    converted = {}

    for field, (value, unit) in data_dict.items():
        expected_unit = expected_dict[field]
        converter = utils.CONVERT_TO_EXPECTED_UNIT.get(field)
        if unit == expected_unit:
            converted[field] = (value, unit)
        elif converter:
            new_value = converter(value, unit)
            converted[field] = (new_value, expected_unit)
        else:
            print(
                f"No conversion rule for '{field}' from '{unit}' to '{expected_unit}', passing through."
            )
            converted[field] = (value, unit)

    return PhenoAgeInput(**converted)


def gompertz_mortality_model(weighted_risk_score: float) -> float:
    __params = levine.Gompertz()
    return 1 - np.exp(
        -np.exp(weighted_risk_score)
        * (np.exp(120 * __params.lambda_) - 1)
        / __params.lambda_
    )


def phenoage(data: PhenoAgeInput) -> tuple[float, float, float]:
    """
    The Phenoage score is calculated as a weighted (coefficients available in Levine et al 2018)
    linear combination of these variables, which was then transformed into units of years using 2 parametric
    (Gompertz distribution) proportional hazard models—one for the linearly combined score for all 10 variables
    and another for chronological age. Thus, PhenoAge represents the expected age within the population that
    corresponds to a person’s estimated hazard of mortality as a function of his/her biological profile.
    """
    __data = convert_to_expected_units(data=data, expected_units=utils.Unit())
    age = data.age[0]
    coef = levine.LinearModel()
    weighted_risk_score = (
        coef.intercept
        + (coef.albumin * __data.albumin[0])
        + (coef.creatinine * __data.creatinine[0])
        + (coef.glucose * __data.glucose[0])
        + (coef.log_crp * __data.log_crp[0])
        + (coef.lymphocyte_percent * __data.lymphocyte_percent[0])
        + (coef.mean_cell_volume * __data.mean_cell_volume[0])
        + (coef.red_cell_distribution_width * __data.red_cell_distribution_width[0])
        + (coef.alkaline_phosphatase * __data.alkaline_phosphatase[0])
        + (coef.white_blood_cell_count * __data.white_blood_cell_count[0])
        + (coef.age * __data.age[0])
    )

    gompertz = gompertz_mortality_model(weighted_risk_score=weighted_risk_score)
    model = levine.Gompertz()
    pred_age = model.coef1 + np.log(model.coef2 * np.log(1 - gompertz)) / model.coef3
    accl_age = pred_age - age
    return (age, pred_age, accl_age)
