import numpy as np
from constants import CONVERT_TO_EXPECTED_UNIT, Coefficients, Gompertz, Unit
from pydantic import BaseModel


class PhenoAgeInput(BaseModel):
    albumin: tuple[float, str]
    creatinine: tuple[float, str]
    glucose: tuple[float, str]
    log_crp: tuple[float, str]
    lymphocyte_percent: tuple[float, str]
    mean_cell_volume: tuple[float, str]
    red_cell_distribution_width: tuple[float, str]
    alkaline_phosphatase: tuple[float, str]
    white_blood_cell_count: tuple[float, str]
    age: tuple[float, str]


def convert_to_expected_units(
    data: PhenoAgeInput, expected_units: Unit
) -> PhenoAgeInput:
    data_dict = data.model_dump()
    expected_dict = expected_units.model_dump()
    converted = {}

    for field, (value, unit) in data_dict.items():
        expected_unit = expected_dict[field]
        converter = CONVERT_TO_EXPECTED_UNIT.get(field)
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
    params = Gompertz()
    return 1 - np.exp(
        -np.exp(weighted_risk_score)
        * (np.exp(120 * params.lambda_) - 1)
        / params.lambda_
    )


def phenoage(data: PhenoAgeInput) -> tuple[float, float, float]:
    """
    The Phenoage score is calculated as a weighted (coefficients available in Levine et al 2018)
    linear combination of these variables, which was then transformed into units of years using 2 parametric
    (Gompertz distribution) proportional hazard models—one for the linearly combined score for all 10 variables
    and another for chronological age. Thus, PhenoAge represents the expected age within the population that
    corresponds to a person’s estimated hazard of mortality as a function of his/her biological profile.
    """
    data = convert_to_expected_units(data=data, expected_units=Unit())
    age = data.age[0]
    cof = Coefficients()
    weighted_risk_score = (
        cof.intercept
        + (cof.albumin * data.albumin[0])
        + (cof.creatinine * data.creatinine[0])
        + (cof.glucose * data.glucose[0])
        + (cof.log_crp * data.log_crp[0])
        + (cof.lymphocyte_percent * data.lymphocyte_percent[0])
        + (cof.mean_cell_volume * data.mean_cell_volume[0])
        + (cof.red_cell_distribution_width * data.red_cell_distribution_width[0])
        + (cof.alkaline_phosphatase * data.alkaline_phosphatase[0])
        + (cof.white_blood_cell_count * data.white_blood_cell_count[0])
        + (cof.age * data.age[0])
    )

    gompertz = gompertz_mortality_model(weighted_risk_score=weighted_risk_score)
    params = Gompertz()
    pred_age = params.coef1 + np.log(params.coef2 * np.log(1 - gompertz)) / params.coef3
    accl_age = age - pred_age
    return (age, pred_age, accl_age)


# if __name__ == "__main__":
# data = PhenoAgeInput(
# albumin=(40.5, "g/L"),
# creatinine=(1.17, "mg/dL"),
# glucose=(70.5, "mg/dL"),
# log_crp=(-0.69, "mg/dl"),
# lymphocyte_percent=(40.3, "%"),
# mean_cell_volume=(89.1, "fL"),
# red_cell_distribution_width=(11.9, "%"),
# alkaline_phosphatase=(63.5, "IU/L"),
# white_blood_cell_count=(6.05, "10^3 cells/uL"),
# age=(39, "years"),
# )
# age, pred_age, accl_age = phenoage(data=data)
# print(f"Age: {age:.2f}, Predicted Age: {pred_age:.2f}, Accelerated Age: {accl_age:.2f}")
