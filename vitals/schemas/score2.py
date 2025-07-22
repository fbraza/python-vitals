from typing import Optional

from pydantic import BaseModel

# Common for all models


class BaselineSurvival(BaseModel):
    """
    Sex-specific baseline survival probabilities for the SCORE2 model.

    These values represent the 10-year survival probability for individuals
    with all risk factors at their reference values.
    """

    male: float = 0.9605
    female: float = 0.9776


class CalibrationScales(BaseModel):
    """
    Region and sex-specific calibration scales for Belgium (Low Risk region).

    These scales are used to calibrate the uncalibrated risk estimate to match
    the population-specific cardiovascular disease incidence rates.
    """

    # Male calibration scales
    male_scale1: float = -0.5699
    male_scale2: float = 0.7476

    # Female calibration scales
    female_scale1: float = -0.7380
    female_scale2: float = 0.7019


# ----- For Basal score2 model


class Markers(BaseModel):
    """Processed Score2 biomarkers with standardized units."""

    age: float
    systolic_blood_pressure: float
    total_cholesterol: float
    hdl_cholesterol: float
    smoking: bool
    is_male: bool
    diabetes: bool | None
    age_at_diabetes_diagnosis: float | None
    hba1c: float | None
    egfr: float | None


class DiabetesMarkers(Markers):
    """Markers with guaranteed non-None diabetes fields for SCORE2-Diabetes algorithm."""

    # Override the optional diabetes fields to be required
    diabetes: bool
    age_at_diabetes_diagnosis: float
    hba1c: float
    egfr: float

    @classmethod
    def try_from_markers(cls, markers: Markers) -> Optional["DiabetesMarkers"]:
        """Factory method to safely create DiabetesMarkers from unified Markers.

        Args:
            markers: Unified Markers instance with potentially None diabetes fields

        Returns:
            DiabetesMarkers instance if all diabetes fields are present and not None,
            None otherwise
        """
        marker_dict = markers.model_dump()

        # Check if all diabetes fields are present and not None
        diabetes_fields = ["diabetes", "age_at_diabetes_diagnosis", "hba1c", "egfr"]
        if all(marker_dict.get(field) is not None for field in diabetes_fields):
            return cls(**marker_dict)
        return None


class Units(BaseModel):
    """
    The expected unit to be used for Score2 computation
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


class MaleCoefficientsBaseModel(BaseModel):
    """
    Male-specific coefficients for the SCORE2 Cox proportional hazards model.
    """

    # Main effects
    age: float = 0.3742
    smoking: float = 0.6012
    sbp: float = 0.2777
    total_cholesterol: float = 0.1458
    hdl_cholesterol: float = -0.2698

    # Age interaction terms
    smoking_age: float = -0.0755
    sbp_age: float = -0.0255
    tchol_age: float = -0.0281
    hdl_age: float = 0.0426


class FemaleCoefficientsBaseModel(BaseModel):
    """
    Female-specific coefficients for the SCORE2 Cox proportional hazards model.
    """

    # Main effects
    age: float = 0.4648
    smoking: float = 0.7744
    sbp: float = 0.3131
    total_cholesterol: float = 0.1002
    hdl_cholesterol: float = -0.2606

    # Age interaction terms
    smoking_age: float = -0.1088
    sbp_age: float = -0.0277
    tchol_age: float = -0.0226
    hdl_age: float = 0.0613


# ----- For Diabetic score2 model


# class MarkersDiabetes(BaseModel):
#     """Processed Score2-Diabetes biomarkers with standardized units."""

#     age: float
#     systolic_blood_pressure: float
#     total_cholesterol: float
#     hdl_cholesterol: float
#     smoking: bool
#     is_male: bool
#     diabetes: bool
#     age_at_diabetes_diagnosis: float
#     hba1c: float
#     egfr: float


# class UnitsDiabetes(BaseModel):
#     """
#     The expected unit to be used for Score2-Diabetes computation
#     """

#     age: str = "years"
#     systolic_blood_pressure: str = "mmHg"
#     total_cholesterol: str = "mmol/L"
#     hdl_cholesterol: str = "mmol/L"
#     smoking: str = "yes/no"
#     is_male: str = "yes/no"
#     diabetes: str = "yes/no"
#     age_at_diabetes_diagnosis: str = "years"
#     hba1c: str = "mmol/mol"
#     egfr: str = "mL/min/1.73m²"


class MaleCoefficientsDiabeticModel(MaleCoefficientsBaseModel):
    """
    Male-specific coefficients for the SCORE2-Diabetes Cox proportional hazards model.
    Extends the base SCORE2 male coefficients with diabetes-specific parameters.
    """

    # Override base values with SCORE2-Diabetes specific values
    age: float = 0.5368
    smoking: float = 0.4774
    sbp: float = 0.1322
    total_cholesterol: float = 0.1102
    hdl_cholesterol: float = -0.1087

    # Override age interaction terms
    smoking_age: float = -0.0672
    sbp_age: float = -0.0268
    tchol_age: float = -0.0181
    hdl_age: float = 0.0095

    # Additional diabetes-specific coefficients
    diabetes: float = 0.6457
    age_at_diabetes_diagnosis: float = -0.0998
    hba1c: float = 0.0955
    egfr: float = -0.0591
    egfr_squared: float = 0.0058

    # Additional age interaction terms
    diabetes_age: float = -0.0983
    hba1c_age: float = -0.0134
    egfr_age: float = 0.0115


class FemaleCoefficientsDiabeticModel(FemaleCoefficientsBaseModel):
    """
    Female-specific coefficients for the SCORE2-Diabetes Cox proportional hazards model.
    Extends the base SCORE2 female coefficients with diabetes-specific parameters.
    """

    # Override base values with SCORE2-Diabetes specific values
    age: float = 0.6624
    smoking: float = 0.6139
    sbp: float = 0.1421
    total_cholesterol: float = 0.1127
    hdl_cholesterol: float = -0.1568

    # Override age interaction terms
    smoking_age: float = -0.1122
    sbp_age: float = -0.0167
    tchol_age: float = -0.0200
    hdl_age: float = 0.0186

    # Additional diabetes-specific coefficients
    diabetes: float = 0.8096
    age_at_diabetes_diagnosis: float = -0.1180
    hba1c: float = 0.1173
    egfr: float = -0.0640
    egfr_squared: float = 0.0062

    # Additional age interaction terms
    diabetes_age: float = -0.1272
    hba1c_age: float = -0.0196
    egfr_age: float = 0.0169
