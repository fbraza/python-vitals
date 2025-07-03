from pathlib import Path

import pytest

from vitals.phenoage import compute

OUT_FILEPATH = Path(__file__).parent / "outputs"


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("test__output__patient_01.json", (39.00, 39.43, 0.43)),
        ("test__output__patient_02.json", (40.00, 40.57, 0.57)),
        ("test__output__patient_03.json", (80.00, 74.78, -5.22)),
        ("test__output__patient_04.json", (36.00, 31.05, -4.95)),
    ],
)
def test_phenoage(filename, expected):
    # Get the actual fixture value using request.getfixturevalue
    age, pred_age, accl_age = compute.biological_age(OUT_FILEPATH / filename)
    expected_age, expected_pred_age, expected_accl_age = expected

    assert age == expected_age
    assert pytest.approx(pred_age, abs=0.02) == expected_pred_age
    assert pytest.approx(accl_age, abs=0.02) == expected_accl_age


if __name__ == "__main__":
    pytest.main([__file__])
