# Vitals

[![PyPI Version][pypi-image]][pypi-url]
[![Build Status][build-image]][build-url]

<!-- Badges -->

[pypi-image]: https://img.shields.io/pypi/v/python-phenoage
[pypi-url]: https://pypi.org/project/python-phenoage/
[build-image]: https://github.com/fbraza/vitals/actions/workflows/ci.yml/badge.svg
[build-url]: https://github.com/fbraza/vitals/blob/master/.github/workflows/ci.yml

## Functionality

`Vitals` is a Python library that implements biomarker algorithms for health assessment, including biological age calculation and cardiovascular disease risk prediction. The library provides robust implementations of scientifically validated algorithms with comprehensive data validation and error handling.

## Setup

To install the package run the following command:

```bash
pip install python-phenoage
```

For development, this project uses UV for dependency management:

```bash
# Clone the repository
git clone https://github.com/fbraza/vitals.git
cd vitals

# Install dependencies
uv sync
```

Once installed, import the algorithms you need:

```python
from vitals.models.phenoage import compute
from vitals.models.score2 import compute
from vitals.models.score2_diabetes import compute
```

## Usage

### PhenoAge

Biological age calculation using Levine's PhenoAge algorithm. This algorithm estimates biological aging based on 10 biomarkers and chronological age.

**Required biomarkers:**
- Albumin (g/dL or g/L)
- Creatinine (mg/dL or ¼mol/L)
- Glucose (mg/dL or mmol/L)
- C-reactive protein (mg/L or mg/dL)
- Lymphocyte percentage (%)
- Mean cell volume (fL)
- Red cell distribution width (%)
- Alkaline phosphatase (U/L)
- White blood cell count (10³/¼L or 10y/L)
- Age (years)

```python
from vitals.models.phenoage import compute

# Example biomarker data
biomarkers = {
    "albumin": 4.2,
    "creatinine": 0.9,
    "glucose": 95,
    "c_reactive_protein": 1.5,
    "lymphocyte_percent": 25,
    "mean_cell_volume": 88,
    "red_cell_distribution_width": 13.2,
    "alkaline_phosphatase": 75,
    "white_blood_cell_count": 6.5,
    "age": 45
}

result = compute(biomarkers)
print(f"Chronological Age: {result.age}")
print(f"Predicted Age: {result.predicted_age:.1f}")
print(f"Accelerated Aging: {result.accelerated_aging:.1f}")
```

### SCORE2

10-year cardiovascular disease risk assessment for non-diabetic European patients aged 40-69 years.

**Required parameters:**
- Age (40-69 years)
- Sex (male/female)
- Systolic blood pressure (mmHg)
- Total cholesterol (mg/dL or mmol/L)
- HDL cholesterol (mg/dL or mmol/L)
- Smoking status (boolean)

```python
from vitals.models.score2 import compute

# Example patient data
biomarkers = {
    "age": 55,
    "sex": "male",
    "systolic_bp": 140,
    "total_cholesterol": 220,
    "hdl_cholesterol": 45,
    "smoking": True
}

result = compute(biomarkers)
print(f"Age: {result.age}")
print(f"CVD Risk: {result.risk_percentage:.1f}%")
print(f"Risk Category: {result.risk_category}")
```

### SCORE2-Diabetes

CVD risk assessment for diabetic patients, including diabetes-specific risk factors.

**Additional parameters for diabetic patients:**
- Diabetes status (boolean)
- Age at diabetes diagnosis (years)
- HbA1c (% or mmol/mol)
- Estimated glomerular filtration rate (mL/min/1.73m²)

```python
from vitals.models.score2_diabetes import compute

# Example diabetic patient data
biomarkers = {
    "age": 60,
    "sex": "female",
    "systolic_bp": 135,
    "total_cholesterol": 200,
    "hdl_cholesterol": 50,
    "smoking": False,
    "diabetes": True,
    "age_diagnosis_diabetes": 45,
    "hba1c": 7.2,
    "egfr": 75
}

result = compute(biomarkers)
print(f"Age: {result.age}")
print(f"CVD Risk: {result.risk_percentage:.1f}%")
print(f"Risk Category: {result.risk_category}")
```

### Working with JSON Data

The library can extract biomarkers from structured JSON files:

```python
from vitals.biomarkers.helpers import extract_biomarkers_from_json
from vitals.models.phenoage import compute

# Load biomarkers from JSON file
with open("patient_data.json", "r") as f:
    json_data = json.load(f)

biomarkers = extract_biomarkers_from_json(json_data, target_biomarkers=[
    "albumin", "creatinine", "glucose", "c_reactive_protein",
    "lymphocyte_percent", "mean_cell_volume", "red_cell_distribution_width",
    "alkaline_phosphatase", "white_blood_cell_count", "age"
])

result = compute(biomarkers)
```

## Features

- **Robust Data Validation**: Uses Pydantic for comprehensive input validation
- **Automatic Unit Conversion**: Handles multiple unit formats automatically
- **Scientific Accuracy**: Implements peer-reviewed algorithms with proper calibrations
- **Type Safety**: Full type hints and mypy compliance
- **Comprehensive Testing**: Extensive test suite with known reference values
- **Error Handling**: Clear error messages for invalid inputs or missing biomarkers

## Algorithms Implemented

### PhenoAge (Levine et al., 2018)
Biological age estimation based on 10 clinical biomarkers. The algorithm was developed using NHANES data and validated across multiple cohorts.

**Reference:** Levine, M.E. et al. An epigenetic biomarker of aging for lifespan and healthspan. Aging (2018).

### SCORE2 (European Society of Cardiology, 2021)
Updated cardiovascular risk prediction algorithm for European populations, calibrated for different risk regions.

**Reference:** SCORE2 working group. SCORE2 risk prediction algorithms. European Heart Journal (2021).

### SCORE2-Diabetes (European Society of Cardiology, 2023)
Diabetes-specific cardiovascular risk assessment incorporating diabetes duration, glycemic control, and kidney function.

**Reference:** SCORE2-Diabetes working group. European Heart Journal (2023).

## For Developers

Clone the repository and set up the development environment:

```bash
git clone https://github.com/fbraza/vitals.git
cd vitals

# Install dependencies and pre-commit hooks
make install

# Run tests
make test

# Run linting
make lint
```

The project uses:
- **UV** for dependency management
- **pytest** for testing with coverage reporting
- **pre-commit** hooks for code quality
- **black** for code formatting
- **mypy** for type checking

All contributions are welcome! Please ensure tests pass and follow the coding guidelines in `specs/coding_style.md`.

## Author

Faouzi Braza
