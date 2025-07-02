import numpy as np
import pytest

from vitals.kdm.compute import KdmInput
from vitals.phenoage.compute import PhenoAgeInput


@pytest.fixture
def patient_01():
    return PhenoAgeInput(
        albumin=(40.5, "g/L"),
        creatinine=(1.17, "mg/dL"),
        glucose=(70.5, "mg/dL"),
        log_crp=(-0.69, "mg/dl"),
        lymphocyte_percent=(40.3, "%"),
        mean_cell_volume=(89.1, "fL"),
        red_cell_distribution_width=(11.9, "%"),
        alkaline_phosphatase=(63.5, "IU/L"),
        white_blood_cell_count=(6.05, "10^3 cells/uL"),
        age=(39, "years"),
    )


@pytest.fixture
def patient_02():
    return PhenoAgeInput(
        albumin=(40, "g/L"),
        creatinine=(51.62659381, "umol/L"),
        glucose=(6.0495, "mmol/L"),
        log_crp=(np.log(0.2099999934), "mg/dl"),
        lymphocyte_percent=(32.34999847, "%"),
        mean_cell_volume=(92.40000153, "fL"),
        red_cell_distribution_width=(12.05000019, "%"),
        alkaline_phosphatase=(59, "IU/L"),
        white_blood_cell_count=(4.949999809, "10^3 cells/uL"),
        age=(40, "years"),
    )


@pytest.fixture
def patient_03():
    return PhenoAgeInput(
        albumin=(40.99999905, "g/L"),
        creatinine=(51.62659381, "umol/L"),
        glucose=(4.9395, "mmol/L"),
        log_crp=(np.log(0.2099999934), "mg/dl"),
        lymphocyte_percent=(43.84999847, "%"),
        mean_cell_volume=(91.90000153, "fL"),
        red_cell_distribution_width=(12.69999981, "%"),
        alkaline_phosphatase=(96, "IU/L"),
        white_blood_cell_count=(4.699999809, "10^3 cells/uL"),
        age=(80, "years"),
    )


@pytest.fixture
def patient_04():
    return PhenoAgeInput(
        albumin=(44.00000095, "g/L"),
        creatinine=(68.5997192, "umol/L"),
        glucose=(4.9395, "mmol/L"),
        log_crp=(np.log(0.2099999934), "mg/dl"),
        lymphocyte_percent=(29, "%"),
        mean_cell_volume=(78.4000015258789, "fL"),
        red_cell_distribution_width=(12.05000019, "%"),
        alkaline_phosphatase=(35, "IU/L"),
        white_blood_cell_count=(5.550000191, "10^3 cells/uL"),
        age=(36, "years"),
    )


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
