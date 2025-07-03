from pydantic import BaseModel


# ------ KDM Schemas
class KdmMarkers(BaseModel):
    """
    Input class for KDM (Klemera-Doubal Method) biological age calculation.

    All biomarkers are optional - KDM can be calculated with any subset of available biomarkers.
    Units should match those expected by the KDM algorithm.
    """

    albumin: float
    alkaline_phosphatase: float
    crp: float
    total_cholesterol: float
    creatinine: float
    hba1c: float
    systolic_blood_pressure: float
    blood_urea_nitrogen: float
    uric_acid: float
    lymphocyte_percent: float
    mean_cell_volume: float
    white_blood_cell_count: float
    age: float  # Chronological age is required


class KdmUnits(BaseModel):
    """
    Expected units for KDM (Klemera-Doubal Method) biological age calculation.
    """

    albumin: str = "g/dL"
    alkaline_phosphatase: str = "U/L"
    crp: str = "mg/dL"
    total_cholesterol: str = "mg/dL"
    creatinine: str = "mg/dL"
    hba1c: str = "%"
    systolic_blood_pressure: str = "mmHg"
    blood_urea_nitrogen: str = "mg/dL"
    uric_acid: str = "mg/dL"
    lymphocyte_percent: str = "%"
    mean_cell_volume: str = "fL"
    white_blood_cell_count: str = "1000 cells/uL"


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
