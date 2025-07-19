from pydantic import BaseModel


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


class Score2Markers(BaseModel):
    """Processed Score2 biomarkers with standardized units."""

    age: float
    systolic_blood_pressure: float
    total_cholesterol: float
    hdl_cholesterol: float
    smoking: bool
    is_male: bool


class Score2DiabetesMarkers(BaseModel):
    """Processed Score2-Diabetes biomarkers with standardized units."""

    age: float
    systolic_blood_pressure: float
    total_cholesterol: float
    hdl_cholesterol: float
    smoking: bool
    is_male: bool
    diabetes: bool
    age_at_diabetes_diagnosis: float
    hba1c: float
    egfr: float
