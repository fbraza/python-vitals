from pathlib import Path

from vitals.biomarkers import helpers
from vitals.schemas import phenoage, score2

INP_FILEPATH_PHENOAGE: Path = Path(__file__).parent / "inputs" / "phenoage"
INP_FILEPATH_SCORE2: Path = Path(__file__).parent / "inputs" / "score2"
INP_FILEPATH_INVALID: Path = Path(__file__).parent / "inputs" / "invalid"


def test_validate_biomarkers_for_algorithm_valid_phenoage():
    """Test successful validation of PhenoAge biomarkers."""
    filepath = INP_FILEPATH_PHENOAGE / "test__input__patient_01.json"
    units = phenoage.Units()

    result = helpers.validate_biomarkers_for_algorithm(
        filepath, phenoage.Markers, units
    )

    assert isinstance(result, phenoage.Markers)
    assert result.albumin == 40.5  # g/L
    assert result.creatinine == 103.428  # umol/L
    assert result.glucose == 3.9167  # mmol/L
    assert result.crp == 0.5  # mg/dL
    assert result.lymphocyte_percent == 40.3  # %
    assert result.mean_cell_volume == 89.1  # fL
    assert result.red_cell_distribution_width == 11.9  # %
    assert result.alkaline_phosphatase == 63.5  # U/L
    assert result.white_blood_cell_count == 6.05  # 1000 cells/uL
    assert result.age == 39  # years


def test_validate_biomarkers_for_algorithm_valid_score2():
    """Test successful validation of SCORE2 biomarkers."""
    filepath = INP_FILEPATH_SCORE2 / "test__input__patient_25.json"
    units = score2.Units()

    result = helpers.validate_biomarkers_for_algorithm(filepath, score2.Markers, units)

    assert isinstance(result, score2.Markers)
    assert result.age == 50
    assert result.systolic_blood_pressure == 140
    assert result.total_cholesterol == 6.3
    assert result.hdl_cholesterol == 1.4
    assert result.smoking is True
    assert result.is_male is False


def test_validate_biomarkers_for_algorithm_missing_phenoage_biomarker():
    """Test validation returns None when required PhenoAge biomarker is missing."""
    filepath = INP_FILEPATH_INVALID / "test__phenoage_missing_albumin.json"
    units = phenoage.Units()

    result = helpers.validate_biomarkers_for_algorithm(
        filepath, phenoage.Markers, units
    )
    assert result is None


def test_validate_biomarkers_for_algorithm_missing_score2_biomarker():
    """Test validation returns None when required SCORE2 biomarker is missing."""
    filepath = INP_FILEPATH_INVALID / "test__score2_missing_sbp.json"
    units = score2.Units()

    result = helpers.validate_biomarkers_for_algorithm(filepath, score2.Markers, units)
    assert result is None
