import pytest

from vitals.phenoage import compute


@pytest.mark.parametrize(
    "patient_fixture,expected",
    [
        ("patient_01", (39.00, 39.43, 0.43)),
        ("patient_02", (40.00, 40.57, 0.57)),
        ("patient_03", (80.00, 74.78, -5.22)),
        ("patient_04", (36.00, 31.05, -4.95)),
    ],
)
def test_phenoage(patient_fixture, expected, request):
    # Get the actual fixture value using request.getfixturevalue
    phenoage_input = request.getfixturevalue(patient_fixture)
    age, pred_age, accl_age = compute.phenoage(phenoage_input)

    expected_age, expected_pred_age, expected_accl_age = expected

    assert age == expected_age
    assert pytest.approx(pred_age, abs=0.01) == expected_pred_age
    assert pytest.approx(accl_age, abs=0.01) == expected_accl_age


if __name__ == "__main__":
    pytest.main([__file__])
