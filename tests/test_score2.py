from pathlib import Path

import pytest

from vitals.score2 import compute

OUT_FILEPATH = Path(__file__).parent / "outputs"


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("test__output__patient_25.json", (50.00, 4.34, "Low to moderate")),
        ("test__output__patient_26.json", (50.00, 6.31, "High")),
    ],
)
def test_score2(filename, expected):
    # Get the actual fixture value using request.getfixturevalue
    age, pred_risk, pred_risk_category = compute.cardiovascular_risk(OUT_FILEPATH / filename)
    expected_age, expected_risk, expected_category = expected

    assert age == expected_age
    assert pred_risk_category == expected_category
    assert pytest.approx(pred_risk, abs=0.1) == expected_risk


if __name__ == "__main__":
    pytest.main([__file__])
