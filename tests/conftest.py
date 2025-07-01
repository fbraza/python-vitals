import numpy as np
import pytest

from phenoage.compute import PhenoAgeInput


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
