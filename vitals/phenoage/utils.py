from collections.abc import Callable

from pydantic import BaseModel


class Unit(BaseModel):
    """
    The expected unit to be used for score computation
    """

    albumin: str = "g/L"
    creatinine: str = "umol/L"
    glucose: str = "mmol/L"
    log_crp: str = "mg/dl"
    lymphocyte_percent: str = "%"
    mean_cell_volume: str = "fL"
    red_cell_distribution_width: str = "%"
    alkaline_phosphatase: str = "IU/L"
    white_blood_cell_count: str = "10^3 cells/uL"
    age: str = "years"


CONVERT_TO_EXPECTED_UNIT: dict[str, Callable[[float, str], float]] = {
    "creatinine": lambda x, u: x * 88.4 if u == "mg/dL" else x,
    "glucose": lambda x, u: x / 18.0 if u == "mg/dL" else x,
    "albumin": lambda x, u: x * 10.0 if u == "g/dL" else x,
    "log_crp": lambda x, u: x / 10.0 if u == "mg/L" else x,
}
