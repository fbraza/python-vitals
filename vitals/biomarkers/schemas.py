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


# ------ SCORE2 Schemas
class Score2Units(BaseModel):
    """
    The expected unit to be used for Score2 computation
    """

    age: str = "years"
    systolic_blood_pressure: str = "mmHg"
    total_cholesterol: str = "mmol/L"
    hdl_cholesterol: str = "mmol/L"
    smoking: str = "yes/no"
    is_male: str = "yes/no"


class Score2Markers(BaseModel):
    """Processed Score2 biomarkers with standardized units."""

    age: float
    systolic_blood_pressure: float
    total_cholesterol: float
    hdl_cholesterol: float
    smoking: bool
    is_male: bool


# ------ SCORE2-Diabetes Schemas
class Score2DiabetesUnits(BaseModel):
    """
    The expected unit to be used for Score2-Diabetes computation
    """

    age: str = "years"
    systolic_blood_pressure: str = "mmHg"
    total_cholesterol: str = "mmol/L"
    hdl_cholesterol: str = "mmol/L"
    smoking: str = "yes/no"
    is_male: str = "yes/no"
    diabetes: str = "yes/no"
    age_at_diabetes_diagnosis: str = "years"
    hba1c: str = "mmol/mol"
    egfr: str = "mL/min/1.73m²"


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
