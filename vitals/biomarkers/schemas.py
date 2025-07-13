from pydantic import BaseModel


# ------ PHENOAGE Schemas
class PhenoageUnits(BaseModel):
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


class PhenoageMarkers(BaseModel):
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
