import numpy as np
import pytest
from compute import (
    PhenoAgeInput,
    convert_to_expected_units,
    gompertz_mortality_model,
    phenoage,
)
from constants import CONVERT_TO_EXPECTED_UNIT, Coefficients, Gompertz, Unit


class TestPhenoAgeInput:
    """Test the PhenoAgeInput model"""

    def test_phenoage_input_valid_data(self):
        """Test creating PhenoAgeInput with valid data"""
        data = PhenoAgeInput(
            albumin=(51.8, "g/L"),
            creatinine=(87.2, "umol/L"),
            glucose=(4.5, "mmol/L"),
            log_crp=(-0.2, "mg/dl"),
            lymphocyte_percent=(27.9, "%"),
            mean_cell_volume=(92.4, "fL"),
            red_cell_distribution_width=(13.9, "%"),
            alkaline_phosphatase=(123.5, "IU/L"),
            white_blood_cell_count=(0.006037, "10^3 cells/uL"),
            age=(70.2, "years"),
        )

        assert data.albumin == (51.8, "g/L")
        assert data.creatinine == (87.2, "umol/L")
        assert data.glucose == (4.5, "mmol/L")
        assert data.log_crp == (-0.2, "mg/dl")
        assert data.lymphocyte_percent == (27.9, "%")
        assert data.mean_cell_volume == (92.4, "fL")
        assert data.red_cell_distribution_width == (13.9, "%")
        assert data.alkaline_phosphatase == (123.5, "IU/L")
        assert data.white_blood_cell_count == (0.006037, "10^3 cells/uL")
        assert data.age == (70.2, "years")

    def test_phenoage_input_missing_field(self):
        """Test that missing required fields raise validation error"""
        with pytest.raises(ValueError):
            PhenoAgeInput(
                albumin=(51.8, "g/L"),
                creatinine=(87.2, "umol/L"),
                glucose=(4.5, "mmol/L"),
                # Missing log_crp
                lymphocyte_percent=(27.9, "%"),
                mean_cell_volume=(92.4, "fL"),
                red_cell_distribution_width=(13.9, "%"),
                alkaline_phosphatase=(123.5, "IU/L"),
                white_blood_cell_count=(0.006037, "10^3 cells/uL"),
                age=(70.2, "years"),
            )


class TestConvertToExpectedUnits:
    """Test the unit conversion functionality"""

    def test_no_conversion_needed(self):
        """Test when all units are already in expected format"""
        data = PhenoAgeInput(
            albumin=(51.8, "g/L"),
            creatinine=(87.2, "umol/L"),
            glucose=(4.5, "mmol/L"),
            log_crp=(-0.2, "mg/dl"),
            lymphocyte_percent=(27.9, "%"),
            mean_cell_volume=(92.4, "fL"),
            red_cell_distribution_width=(13.9, "%"),
            alkaline_phosphatase=(123.5, "IU/L"),
            white_blood_cell_count=(0.006037, "10^3 cells/uL"),
            age=(70.2, "years"),
        )

        expected_units = Unit()
        converted = convert_to_expected_units(data, expected_units)

        # Should be identical since no conversion needed
        assert converted.albumin == data.albumin
        assert converted.creatinine == data.creatinine
        assert converted.glucose == data.glucose
        assert converted.log_crp == data.log_crp

    def test_creatinine_conversion_mg_dl_to_umol_l(self):
        """Test creatinine conversion from mg/dL to umol/L"""
        data = PhenoAgeInput(
            albumin=(51.8, "g/L"),
            creatinine=(1.0, "mg/dL"),  # Different unit
            glucose=(4.5, "mmol/L"),
            log_crp=(-0.2, "mg/dl"),
            lymphocyte_percent=(27.9, "%"),
            mean_cell_volume=(92.4, "fL"),
            red_cell_distribution_width=(13.9, "%"),
            alkaline_phosphatase=(123.5, "IU/L"),
            white_blood_cell_count=(0.006037, "10^3 cells/uL"),
            age=(70.2, "years"),
        )

        expected_units = Unit()
        converted = convert_to_expected_units(data, expected_units)

        # 1.0 mg/dL * 88.4 = 88.4 umol/L
        assert converted.creatinine == (88.4, "umol/L")

    def test_glucose_conversion_mg_dl_to_mmol_l(self):
        """Test glucose conversion from mg/dL to mmol/L"""
        data = PhenoAgeInput(
            albumin=(51.8, "g/L"),
            creatinine=(87.2, "umol/L"),
            glucose=(90.0, "mg/dL"),  # Different unit
            log_crp=(-0.2, "mg/dl"),
            lymphocyte_percent=(27.9, "%"),
            mean_cell_volume=(92.4, "fL"),
            red_cell_distribution_width=(13.9, "%"),
            alkaline_phosphatase=(123.5, "IU/L"),
            white_blood_cell_count=(0.006037, "10^3 cells/uL"),
            age=(70.2, "years"),
        )

        expected_units = Unit()
        converted = convert_to_expected_units(data, expected_units)

        # 90.0 mg/dL / 18.0 = 5.0 mmol/L
        assert converted.glucose == (5.0, "mmol/L")

    def test_albumin_conversion_g_dl_to_g_l(self):
        """Test albumin conversion from g/dL to g/L"""
        data = PhenoAgeInput(
            albumin=(5.18, "g/dL"),  # Different unit
            creatinine=(87.2, "umol/L"),
            glucose=(4.5, "mmol/L"),
            log_crp=(-0.2, "mg/dl"),
            lymphocyte_percent=(27.9, "%"),
            mean_cell_volume=(92.4, "fL"),
            red_cell_distribution_width=(13.9, "%"),
            alkaline_phosphatase=(123.5, "IU/L"),
            white_blood_cell_count=(0.006037, "10^3 cells/uL"),
            age=(70.2, "years"),
        )

        expected_units = Unit()
        converted = convert_to_expected_units(data, expected_units)

        # 5.18 g/dL * 10.0 = 51.8 g/L
        assert converted.albumin == (51.8, "g/L")

    def test_log_crp_conversion_mg_l_to_mg_dl(self):
        """Test log_crp conversion from mg/L to mg/dl"""
        data = PhenoAgeInput(
            albumin=(51.8, "g/L"),
            creatinine=(87.2, "umol/L"),
            glucose=(4.5, "mmol/L"),
            log_crp=(-2.0, "mg/L"),  # Different unit
            lymphocyte_percent=(27.9, "%"),
            mean_cell_volume=(92.4, "fL"),
            red_cell_distribution_width=(13.9, "%"),
            alkaline_phosphatase=(123.5, "IU/L"),
            white_blood_cell_count=(0.006037, "10^3 cells/uL"),
            age=(70.2, "years"),
        )

        expected_units = Unit()
        converted = convert_to_expected_units(data, expected_units)

        # -2.0 mg/L / 10.0 = -0.2 mg/dl
        assert converted.log_crp == (-0.2, "mg/dl")


class TestGompertzMortalityModel:
    """Test the Gompertz mortality model function"""

    def test_gompertz_with_zero_score(self):
        """Test Gompertz model with zero weighted risk score"""
        result = gompertz_mortality_model(0.0)
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_gompertz_with_positive_score(self):
        """Test Gompertz model with positive weighted risk score"""
        result = gompertz_mortality_model(1.0)
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_gompertz_with_negative_score(self):
        """Test Gompertz model with negative weighted risk score"""
        result = gompertz_mortality_model(-1.0)
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_gompertz_with_large_score(self):
        """Test Gompertz model with large weighted risk score"""
        result = gompertz_mortality_model(10.0)
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_gompertz_calculation_accuracy(self):
        """Test specific calculation with known values"""
        # Test with a specific value to ensure calculation is correct
        weighted_risk_score = 2.0
        params = Gompertz()
        expected = 1 - np.exp(
            -np.exp(weighted_risk_score)
            * (np.exp(120 * params.lambda_) - 1)
            / params.lambda_
        )
        result = gompertz_mortality_model(weighted_risk_score)
        assert abs(result - expected) < 1e-10


class TestPhenoage:
    """Test the main phenoage function"""

    def test_phenoage_calculation_basic(self):
        """Test basic phenoage calculation with standard input"""
        data = PhenoAgeInput(
            albumin=(51.8, "g/L"),
            creatinine=(87.2, "umol/L"),
            glucose=(4.5, "mmol/L"),
            log_crp=(-0.2, "mg/dl"),
            lymphocyte_percent=(27.9, "%"),
            mean_cell_volume=(92.4, "fL"),
            red_cell_distribution_width=(13.9, "%"),
            alkaline_phosphatase=(123.5, "IU/L"),
            white_blood_cell_count=(0.006037, "10^3 cells/uL"),
            age=(70.2, "years"),
        )

        age, pred_age, accl_age = phenoage(data)

        assert isinstance(age, float)
        assert isinstance(pred_age, float)
        assert isinstance(accl_age, float)
        assert age == 70.2  # Should match input age

    def test_phenoage_with_unit_conversion(self):
        """Test phenoage with input requiring unit conversion"""
        data = PhenoAgeInput(
            albumin=(5.18, "g/dL"),  # Will be converted to g/L
            creatinine=(1.0, "mg/dL"),  # Will be converted to umol/L
            glucose=(81.0, "mg/dL"),  # Will be converted to mmol/L
            log_crp=(-2.0, "mg/L"),  # Will be converted to mg/dl
            lymphocyte_percent=(27.9, "%"),
            mean_cell_volume=(92.4, "fL"),
            red_cell_distribution_width=(13.9, "%"),
            alkaline_phosphatase=(123.5, "IU/L"),
            white_blood_cell_count=(0.006037, "10^3 cells/uL"),
            age=(70.2, "years"),
        )

        age, pred_age, accl_age = phenoage(data)

        assert isinstance(age, float)
        assert isinstance(pred_age, float)
        assert isinstance(accl_age, float)
        assert age == 70.2

    def test_phenoage_young_age(self):
        """Test phenoage with young age input"""
        data = PhenoAgeInput(
            albumin=(51.8, "g/L"),
            creatinine=(87.2, "umol/L"),
            glucose=(4.5, "mmol/L"),
            log_crp=(-0.2, "mg/dl"),
            lymphocyte_percent=(27.9, "%"),
            mean_cell_volume=(92.4, "fL"),
            red_cell_distribution_width=(13.9, "%"),
            alkaline_phosphatase=(123.5, "IU/L"),
            white_blood_cell_count=(0.006037, "10^3 cells/uL"),
            age=(25.0, "years"),
        )

        age, pred_age, accl_age = phenoage(data)

        assert age == 25.0
        assert isinstance(pred_age, float)
        assert isinstance(accl_age, float)

    def test_phenoage_elderly_age(self):
        """Test phenoage with elderly age input"""
        data = PhenoAgeInput(
            albumin=(51.8, "g/L"),
            creatinine=(87.2, "umol/L"),
            glucose=(4.5, "mmol/L"),
            log_crp=(-0.2, "mg/dl"),
            lymphocyte_percent=(27.9, "%"),
            mean_cell_volume=(92.4, "fL"),
            red_cell_distribution_width=(13.9, "%"),
            alkaline_phosphatase=(123.5, "IU/L"),
            white_blood_cell_count=(0.006037, "10^3 cells/uL"),
            age=(95.0, "years"),
        )

        age, pred_age, accl_age = phenoage(data)

        assert age == 95.0
        assert isinstance(pred_age, float)
        assert isinstance(accl_age, float)

    def test_phenoage_extreme_biomarker_values(self):
        """Test phenoage with extreme biomarker values"""
        data = PhenoAgeInput(
            albumin=(20.0, "g/L"),  # Low albumin
            creatinine=(200.0, "umol/L"),  # High creatinine
            glucose=(15.0, "mmol/L"),  # High glucose
            log_crp=(3.0, "mg/dl"),  # High CRP
            lymphocyte_percent=(5.0, "%"),  # Low lymphocytes
            mean_cell_volume=(110.0, "fL"),  # High MCV
            red_cell_distribution_width=(20.0, "%"),  # High RDW
            alkaline_phosphatase=(300.0, "IU/L"),  # High ALP
            white_blood_cell_count=(15.0, "10^3 cells/uL"),  # High WBC
            age=(70.0, "years"),
        )

        age, pred_age, accl_age = phenoage(data)

        assert age == 70.0
        assert isinstance(pred_age, float)
        assert isinstance(accl_age, float)
        # With poor biomarkers, predicted age should likely be higher than chronological age
        assert pred_age > age

    def test_phenoage_optimal_biomarker_values(self):
        """Test phenoage with optimal biomarker values"""
        data = PhenoAgeInput(
            albumin=(55.0, "g/L"),  # High albumin
            creatinine=(60.0, "umol/L"),  # Low creatinine
            glucose=(4.0, "mmol/L"),  # Normal glucose
            log_crp=(-2.0, "mg/dl"),  # Low CRP
            lymphocyte_percent=(40.0, "%"),  # High lymphocytes
            mean_cell_volume=(85.0, "fL"),  # Normal MCV
            red_cell_distribution_width=(12.0, "%"),  # Low RDW
            alkaline_phosphatase=(50.0, "IU/L"),  # Low ALP
            white_blood_cell_count=(5.0, "10^3 cells/uL"),  # Normal WBC
            age=(70.0, "years"),
        )

        age, pred_age, accl_age = phenoage(data)

        assert age == 70.0
        assert isinstance(pred_age, float)
        assert isinstance(accl_age, float)
        # With good biomarkers, predicted age should likely be lower than chronological age
        assert pred_age < age


class TestConstants:
    """Test the constants and their values"""

    def test_coefficients_values(self):
        """Test that coefficients have expected values"""
        coeff = Coefficients()
        assert coeff.intercept == -19.9067
        assert coeff.albumin == -0.0336
        assert coeff.creatinine == 0.0095
        assert coeff.glucose == 0.1953
        assert coeff.log_crp == 0.0954
        assert coeff.lymphocyte_percent == -0.0120
        assert coeff.mean_cell_volume == 0.0268
        assert coeff.red_cell_distribution_width == 0.3306
        assert coeff.alkaline_phosphatase == 0.00188
        assert coeff.white_blood_cell_count == 0.0554
        assert coeff.age == 0.0804

    def test_unit_values(self):
        """Test that units have expected values"""
        unit = Unit()
        assert unit.albumin == "g/L"
        assert unit.creatinine == "umol/L"
        assert unit.glucose == "mmol/L"
        assert unit.log_crp == "mg/dl"
        assert unit.lymphocyte_percent == "%"
        assert unit.mean_cell_volume == "fL"
        assert unit.red_cell_distribution_width == "%"
        assert unit.alkaline_phosphatase == "IU/L"
        assert unit.white_blood_cell_count == "10^3 cells/uL"
        assert unit.age == "years"

    def test_gompertz_values(self):
        """Test that Gompertz parameters have expected values"""
        gompertz = Gompertz()
        assert gompertz.lambda_ == 0.0192
        assert gompertz.coef1 == 141.50225
        assert gompertz.coef2 == -0.00553
        assert gompertz.coef3 == 0.090165

    def test_conversion_functions(self):
        """Test unit conversion functions"""
        # Test creatinine conversion
        assert CONVERT_TO_EXPECTED_UNIT["creatinine"](1.0, "mg/dL") == 88.4
        assert CONVERT_TO_EXPECTED_UNIT["creatinine"](88.4, "umol/L") == 88.4

        # Test glucose conversion
        assert CONVERT_TO_EXPECTED_UNIT["glucose"](90.0, "mg/dL") == 5.0
        assert CONVERT_TO_EXPECTED_UNIT["glucose"](5.0, "mmol/L") == 5.0

        # Test albumin conversion
        assert CONVERT_TO_EXPECTED_UNIT["albumin"](5.0, "g/dL") == 50.0
        assert CONVERT_TO_EXPECTED_UNIT["albumin"](50.0, "g/L") == 50.0

        # Test log_crp conversion
        assert CONVERT_TO_EXPECTED_UNIT["log_crp"](10.0, "mg/L") == 1.0
        assert CONVERT_TO_EXPECTED_UNIT["log_crp"](1.0, "mg/dl") == 1.0


if __name__ == "__main__":
    pytest.main([__file__])
