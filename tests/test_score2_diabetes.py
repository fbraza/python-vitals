from pathlib import Path

import pytest

from vitals.score2_diabetes import compute

OUT_FILEPATH = Path(__file__).parent / "inputs" / "score2_diabetes"


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("test__input__patient_01.json", (45.00, 0.00, "PLACEHOLDER")),
        ("test__input__patient_02.json", (55.00, 0.00, "PLACEHOLDER")),
        ("test__input__patient_03.json", (65.00, 0.00, "PLACEHOLDER")),
        ("test__input__patient_04.json", (48.00, 0.00, "PLACEHOLDER")),
        ("test__input__patient_05.json", (60.00, 0.00, "PLACEHOLDER")),
        ("test__input__patient_06.json", (42.00, 0.00, "PLACEHOLDER")),
    ],
)
def test_score2_diabetes(filename, expected):
    """
    Test SCORE2-Diabetes cardiovascular risk calculation.

    NOTE: The expected risk values and categories are placeholders.
    They need to be calculated using MDCalc and updated before running tests.
    """
    # Get the actual fixture value
    age, pred_risk, pred_risk_category = compute.cardiovascular_risk(
        OUT_FILEPATH / filename
    )
    expected_age, expected_risk, expected_category = expected

    assert age == expected_age
    # TODO: Update these assertions once actual values are calculated
    # assert pred_risk_category == expected_category
    # assert pytest.approx(pred_risk, abs=0.1) == expected_risk


if __name__ == "__main__":
    pytest.main([__file__])
