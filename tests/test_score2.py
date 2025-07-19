from pathlib import Path

import pytest

from vitals.models import score2

OUT_FILEPATH = Path(__file__).parent / "inputs" / "score2"


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("test__input__patient_25.json", (50.00, 4.34, "Low to moderate")),
        ("test__input__patient_26.json", (50.00, 6.31, "High")),
        ("test__input__patient_27.json", (55.00, 2.10, "Low to moderate")),
        ("test__input__patient_28.json", (45.00, 2.40, "Low to moderate")),
        ("test__input__patient_29.json", (40.00, 4.30, "High")),
        ("test__input__patient_30.json", (60.00, 4.20, "Low to moderate")),
        ("test__input__patient_31.json", (65.00, 14.40, "Very high")),
        ("test__input__patient_32.json", (69.00, 8.40, "High")),
        ("test__input__patient_33.json", (49.00, 5.70, "High")),
        ("test__input__patient_34.json", (50.00, 1.20, "Low to moderate")),
        ("test__input__patient_35.json", (55.00, 8.70, "High")),
        ("test__input__patient_36.json", (45.00, 2.60, "High")),
    ],
)
def test_score2(filename, expected):
    # Get the actual fixture value using request.getfixturevalue
    age, pred_risk, pred_risk_category = score2.compute(OUT_FILEPATH / filename)
    expected_age, expected_risk, expected_category = expected

    assert age == expected_age
    assert pred_risk_category == expected_category
    assert pytest.approx(pred_risk, abs=0.1) == expected_risk


if __name__ == "__main__":
    pytest.main([__file__])
