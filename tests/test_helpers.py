from pathlib import Path

import pytest

from vitals.biomarkers import exceptions, helpers
from vitals.schemas import phenoage, score2

INP_FILEPATH_PHENOAGE: Path = Path(__file__).parent / "inputs" / "phenoage"
INP_FILEPATH_SCORE2: Path = Path(__file__).parent / "inputs" / "score2"
INP_FILEPATH_INVALID: Path = Path(__file__).parent / "inputs" / "invalid"


def test_extract_biomarkers_from_json_valid_phenoage():
    """Test successful extraction of PhenoAge biomarkers."""
    filepath = INP_FILEPATH_PHENOAGE / "test__input__patient_01.json"
    units = phenoage.Units()

    result = helpers.extract_biomarkers_from_json(filepath, phenoage.Markers, units)

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


def test_extract_biomarkers_from_json_valid_score2():
    """Test successful extraction of SCORE2 biomarkers."""
    filepath = INP_FILEPATH_SCORE2 / "test__input__patient_25.json"
    units = score2.Units()

    result = helpers.extract_biomarkers_from_json(filepath, score2.Markers, units)

    assert isinstance(result, score2.Markers)
    assert result.age == 50
    assert result.systolic_blood_pressure == 140
    assert result.total_cholesterol == 6.3
    assert result.hdl_cholesterol == 1.4
    assert result.smoking is True
    assert result.is_male is False


def test_extract_biomarkers_from_json_missing_phenoage_biomarker():
    """Test extraction fails when required PhenoAge biomarker is missing."""
    filepath = INP_FILEPATH_INVALID / "test__phenoage_missing_albumin.json"
    units = phenoage.Units()

    with pytest.raises(
        exceptions.BiomarkerNotFound,
        match="Biomarker 'albumin' not found : Stop computation",
    ):
        helpers.extract_biomarkers_from_json(filepath, phenoage.Markers, units)


def test_extract_biomarkers_from_json_missing_score2_biomarker():
    """Test extraction fails when required SCORE2 biomarker is missing."""
    filepath = INP_FILEPATH_INVALID / "test__score2_missing_sbp.json"
    units = score2.Units()

    with pytest.raises(
        exceptions.BiomarkerNotFound,
        match="Biomarker 'systolic_blood_pressure' not found : Stop computation",
    ):
        helpers.extract_biomarkers_from_json(filepath, score2.Markers, units)
