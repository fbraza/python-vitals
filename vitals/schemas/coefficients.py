from pydantic import BaseModel


class Score2MaleCoefficients(BaseModel):
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


class Score2FemaleCoefficients(BaseModel):
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


class Score2DiabetesMaleCoefficients(Score2MaleCoefficients):
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


class Score2DiabetesFemaleCoefficients(Score2FemaleCoefficients):
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
