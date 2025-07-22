import json
from pathlib import Path

import pytest

from vitals.biomarkers import helpers
from vitals.models import phenoage
from vitals.schemas.phenoage import Markers, Units

OUT_FILEPATH = Path(__file__).parent / "inputs" / "phenoage"


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("test__input__patient_01.json", (39.00, 39.43, 0.43)),
        ("test__input__patient_02.json", (40.00, 40.57, 0.57)),
        ("test__input__patient_03.json", (80.00, 74.78, -5.22)),
        ("test__input__patient_04.json", (36.00, 31.05, -4.95)),
        ("test__input__patient_05.json", (35.00, 39.42, 4.42)),
        ("test__input__patient_06.json", (42.00, 53.71, 11.71)),
        ("test__input__patient_07.json", (36.00, 31.06, -4.94)),
        ("test__input__patient_08.json", (31.00, 31.64, 0.65)),
        ("test__input__patient_17.json", (53.00, 52.86, -0.14)),
        ("test__input__patient_19.json", (70.00, 78.85, 8.85)),
        ("test__input__patient_23.json", (62.00, 61.75, -0.25)),
    ],
)
def test_phenoage(filename, expected):
    # Get the actual fixture value using request.getfixturevalue
    with open(OUT_FILEPATH / filename) as f:
        test__input = json.load(f)
        test_biomarkers = helpers.validate_biomarkers_for_algorithm(
            raw_biomarkers=test__input, biomarker_class=Markers, biomarker_units=Units()
        )
        if test_biomarkers is not None:
            age, pred_age, accl_age = phenoage.compute(test_biomarkers)
            expected_age, expected_pred_age, expected_accl_age = expected

            assert age == expected_age
            assert pytest.approx(pred_age, abs=0.5) == expected_pred_age
            assert pytest.approx(accl_age, abs=0.02) == expected_accl_age


if __name__ == "__main__":
    pytest.main([__file__])
