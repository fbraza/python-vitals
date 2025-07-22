from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from vitals.biomarkers import helpers
from vitals.biomarkers.helpers import RiskCategory
from vitals.models import phenoage, score2, score2_diabetes
from vitals.schemas.phenoage import Markers as PhenoAgeMarkers
from vitals.schemas.phenoage import Units as PhenoAgeUnits
from vitals.schemas.score2 import DiabetesMarkers
from vitals.schemas.score2 import Markers as Score2Markers
from vitals.schemas.score2 import Units as Score2Units


class PatientMetadata(BaseModel):
    """Patient metadata information."""

    patient_id: str
    sex: str
    timestamp: str
    test_date: str
    laboratory: str


class RawBiomarkerData(BaseModel):
    """Raw biomarker data payload from mobile app."""

    metadata: PatientMetadata
    raw_biomarkers: dict[str, dict[str, Any]]


class PhenoAgeResult(BaseModel):
    """PhenoAge calculation results."""

    algorithm: str = "phenoage"
    chronological_age: float
    predicted_age: float
    accelerated_aging: float


class Score2Result(BaseModel):
    """SCORE2 calculation results."""

    algorithm: str = "score2"
    age: float
    calibrated_risk_percent: float
    risk_category: RiskCategory


class Score2DiabetesResult(BaseModel):
    """SCORE2-Diabetes calculation results."""

    algorithm: str = "scores2_diabetes"
    age: float
    calibrated_risk_percent: float
    risk_category: RiskCategory


class BiomarkerResponse(BaseModel):
    """Response containing calculated biomarker results."""

    patient_id: str
    results: dict[str, Any] = Field(default_factory=dict)
    processed_algorithms: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    """Error response for validation failures."""

    error: str
    detail: str


# Create FastAPI application
app = FastAPI(
    title="Vitals Biomarker API",
    description="API for processing biomarker data and calculating health scores (PhenoAge, SCORE2, SCORE2-Diabetes)",
    version="1.0.0",
)


@app.post("/process_data", response_model=BiomarkerResponse)
async def process_data(data: RawBiomarkerData) -> BiomarkerResponse:
    """
    Process biomarker data and calculate health scores.

    This endpoint accepts biomarker data from mobile applications and processes it
    through available algorithms (PhenoAge, SCORE2, SCORE2-Diabetes) based on
    the biomarkers present in the payload.

    Args:
        data: Raw biomarker data with metadata and biomarker values

    Returns:
        BiomarkerResponse with calculated results from applicable algorithms
    """
    response = BiomarkerResponse(
        patient_id=data.metadata.patient_id,
        results={},
        processed_algorithms=[],
        errors=[],
    )

    # Add converted biomarkers (e.g., mg/dL to mmol/L conversions)
    converted_biomarkers = helpers.add_converted_biomarkers(data.raw_biomarkers)

    # ---- PHENOAGE
    phenoage_markers = helpers.validate_biomarkers_for_algorithm(
        raw_biomarkers=converted_biomarkers,
        biomarker_class=PhenoAgeMarkers,
        biomarker_units=PhenoAgeUnits(),
    )
    if phenoage_markers is not None:
        chrono_age, pred_age, accl_age = phenoage.compute(phenoage_markers)
        phenoage_data: PhenoAgeResult = PhenoAgeResult(
            chronological_age=chrono_age,
            predicted_age=pred_age,
            accelerated_aging=accl_age,
        )
        response.results["phenoage"] = phenoage_data.model_dump()
        response.processed_algorithms.append(phenoage_data.algorithm)
    else:
        response.results["phenoage"] = None
        response.errors.append("PhenoAge not computer: Missing required biomarkers")

    # ---- SCORE2 (all variants)
    score2_markers = helpers.validate_biomarkers_for_algorithm(
        raw_biomarkers=converted_biomarkers,
        biomarker_class=Score2Markers,
        biomarker_units=Score2Units(),
    )

    score2_data: Score2DiabetesResult | Score2Result | None = None
    if score2_markers is not None:
        age: float = score2_markers.age
        scores2_with_diabetes_markers: DiabetesMarkers | None = (
            DiabetesMarkers.try_from_markers(score2_markers)
        )

        if age >= 70 and scores2_with_diabetes_markers is not None:
            # Future implementation for older people
            response.errors.append(
                "SCORE2 for older people (age ≥ 70) not yet implemented"
            )
        elif 40 <= age <= 69:
            if scores2_with_diabetes_markers is not None:
                age, calibrated_risk, risk_category = score2_diabetes.compute(
                    scores2_with_diabetes_markers
                )
                score2_data = Score2DiabetesResult(
                    age=age,  # Note: First value is age, not risk_score
                    calibrated_risk_percent=calibrated_risk,
                    risk_category=risk_category,
                )
            else:
                # Use standard SCORE2 algorithm
                age, calibrated_risk, risk_category = score2.compute(score2_markers)
                score2_data = Score2Result(
                    age=age,  # Note: First value is age, not risk_score
                    calibrated_risk_percent=calibrated_risk,
                    risk_category=risk_category,
                )

    # Store result if calculation was successful
    if score2_data:
        response.results[score2_data.algorithm] = score2_data.model_dump()
        response.processed_algorithms.append(score2_data.algorithm)
    else:
        response.results["score2"] = None
        response.errors.append(
            "SCORE2 not: Missing required biomarkers or Age requirements no"
        )

    return response


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Vitals Biomarker API",
        "version": "1.0.0",
        "endpoints": {
            "/process_data": "POST - Process biomarker data",
            "/docs": "GET - API documentation",
            "/redoc": "GET - Alternative API documentation",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
