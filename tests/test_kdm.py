"""Tests for the KDM (Klemera-Doubal Method) biological age calculation."""

import pytest

from vitals.kdm import compute


@pytest.mark.parametrize(
    "patient_fixture,sex,expected_pred_age",
    [
        ("kdm_patient1_full", "female", 49.83),
        ("kdm_patient2_full", "male", 37.86),
        (
            "kdm_patient1_phenoage_only",
            "female",
            28.89,
        ),  # No expected value for reduced set
        (
            "kdm_patient2_phenoage_only",
            "male",
            33.82,
        ),  # No expected value for reduced set
    ],
)
def test_kdm_calculation(patient_fixture, sex, expected_pred_age, request):
    """Test KDM calculation for various patient scenarios."""
    patient = request.getfixturevalue(patient_fixture)
    _, pred_age, accl_age = compute.kdm_age(patient, sex=sex)

    assert pytest.approx(pred_age, abs=0.01) == expected_pred_age
