from pydantic import BaseModel


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


class Unit(BaseModel):
    """
    The expected unit to be used for phenoage computation
    """

    albumin: str = "g/L"
    creatinine: str = "umol/L"
    glucose: str = "mmol/L"
    crp: str = "mg/dL"
    lymphocyte_percent: str = "%"
    mean_cell_volume: str = "fL"
    red_cell_distribution_width: str = "%"
    alkaline_phosphatase: str = "U/L"
    white_blood_cell_count: str = "1000 cells/uL"
    age: str = "years"
