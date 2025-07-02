import pytest

from vitals.kdm.compute import KdmInput


# KDM Test Fixtures
@pytest.fixture
def kdm_patient1_full():
    """48-year-old female with all biomarkers"""
    return KdmInput(
        albumin=4.0,
        alkaline_phosphatase=59.0,
        log_crp=0.1906203542,
        total_cholesterol=236.0,
        log_creatinine=0.4599533006,
        hba1c=5.300000191,
        systolic_blood_pressure=131.0,
        blood_urea_nitrogen=14.0,
        uric_acid=5.0,
        lymphocyte_percent=32.34999847,
        mean_cell_volume=92.40000153,
        white_blood_cell_count=4.949999809,
        age=48.0,
    )


@pytest.fixture
def kdm_patient2_full():
    """35-year-old male with all biomarkers"""
    return KdmInput(
        albumin=4.5,
        alkaline_phosphatase=74.0,
        log_crp=0.1906203542,
        total_cholesterol=225.0,
        log_creatinine=0.6770178219,
        hba1c=4.599999905,
        systolic_blood_pressure=130.0,
        blood_urea_nitrogen=14.0,
        uric_acid=6.400000095,
        lymphocyte_percent=27.20000076,
        mean_cell_volume=90.40000153,
        white_blood_cell_count=5.900000095,
        age=35.0,
    )


@pytest.fixture
def kdm_patient1_phenoage_only():
    """48-year-old female with only PhenoAge biomarkers"""
    return KdmInput(
        albumin=4.0,
        alkaline_phosphatase=59.0,
        log_crp=0.1906203542,
        total_cholesterol=None,
        log_creatinine=0.4599533006,
        hba1c=None,
        systolic_blood_pressure=None,
        blood_urea_nitrogen=None,
        uric_acid=None,
        lymphocyte_percent=32.34999847,
        mean_cell_volume=92.40000153,
        white_blood_cell_count=4.949999809,
        age=48.0,
    )


@pytest.fixture
def kdm_patient2_phenoage_only():
    """35-year-old male with only PhenoAge biomarkers"""
    return KdmInput(
        albumin=4.5,
        alkaline_phosphatase=74.0,
        log_crp=0.1906203542,
        total_cholesterol=None,
        log_creatinine=0.6770178219,
        hba1c=None,
        systolic_blood_pressure=None,
        blood_urea_nitrogen=None,
        uric_acid=None,
        lymphocyte_percent=27.20000076,
        mean_cell_volume=90.40000153,
        white_blood_cell_count=5.900000095,
        age=35.0,
    )
