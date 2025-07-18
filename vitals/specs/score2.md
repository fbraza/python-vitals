# CVD Risk Prediction Formula

## Overview

This formula calculates the 10-year risk of cardiovascular disease (CVD) using a sex-specific Cox proportional hazards model. The model incorporates multiple risk factors with specific transformations and interaction terms to provide personalized risk estimates.

**Target Population**: European patients aged 40-69 years without prior CVD or diabetes.

## Model Coefficients and Baseline Survival

The model coefficients and baseline survival to calculate 10-year risk of CVD are as follows:

| Risk Factor | Transformation | Male | Female |
|-------------|----------------|------|--------|
| Age, years | cage = (age - 60)/5 | 0.3742 | 0.4648 |
| Smoking | current = 1, other = 0 | 0.6012 | 0.7744 |
| SBP, mm Hg | csbp = (sbp - 120)/20 | 0.2777 | 0.3131 |
| Total cholesterol, mmol/L | ctchol = tchol - 6 | 0.1458 | 0.1002 |
| HDL cholesterol, mmol/L | chdl = (hdl - 1.3)/0.5 | -0.2698 | -0.2606 |
| Smoking*age interaction | smoking*cage | -0.0755 | -0.1088 |
| SBP*age interaction | csbp*cage | -0.0255 | -0.0277 |
| Total cholesterol*age interaction | ctchol*cage | -0.0281 | -0.0226 |
| HDL cholesterol*age interaction | chdl*cage | 0.0426 | 0.0613 |
| **Baseline survival** | | **0.9605** | **0.9776** |

## Risk Calculation Formula

The uncalibrated 10-year risk of CVD is calculated by the following:

**10-year risk = 1 - (baseline survival)^exp(x)**

where **x = Σ[β*(transformed variables)]**

## Regional Calibration

The region and sex-specific scales to calculate calibrated 10-year risk are as follows:

| Risk Region | Male Scale 1 | Male Scale 2 | Female Scale 1 | Female Scale 2 |
|-------------|--------------|--------------|----------------|----------------|
| Low | -0.5699 | 0.7476 | -0.7380 | 0.7019 |
| Moderate | -0.1565 | 0.8009 | -0.3143 | 0.7701 |
| High | 0.3207 | 0.9360 | 0.5710 | 0.9369 |
| Very high | 0.5836 | 0.8294 | 0.9412 | 0.8329 |

### Calibrated Risk Calculation Formula

The calibrated 10-year risk of CVD is calculated by the following:

**Calibrated 10-year risk, % = [1 - exp(-exp(scale1 + scale2*ln(-ln(1 - 10-year risk))))] * 100**

### Regional Risk Classification

- **Belgium**: Classified as a **Low Risk** region
- For initial development, use the Low Risk calibration scales:
  - Males: Scale 1 = -0.5699, Scale 2 = 0.7476
  - Females: Scale 1 = -0.7380, Scale 2 = 0.7019

## Model Components Explained

### Risk Factor Transformations

1. **Age (cage)**: Centered at 60 years and scaled by 5-year intervals
   - `cage = (age - 60)/5`

2. **Smoking**: Binary indicator
   - `current = 1, other = 0`

3. **Systolic Blood Pressure (csbp)**: Centered at 120 mmHg and scaled by 20 mmHg intervals
   - `csbp = (sbp - 120)/20`

4. **Total Cholesterol (ctchol)**: Centered at 6 mmol/L
   - `ctchol = tchol - 6`

5. **HDL Cholesterol (chdl)**: Centered at 1.3 mmol/L and scaled by 0.5 mmol/L intervals
   - `chdl = (hdl - 1.3)/0.5`

### Interaction Terms

The model includes four age interaction terms that capture how the effect of risk factors changes with age:

1. **Smoking × Age**: `smoking × cage`
2. **SBP × Age**: `csbp × cage`
3. **Total Cholesterol × Age**: `ctchol × cage`
4. **HDL Cholesterol × Age**: `chdl × cage`

### Sex-Specific Differences

- **Females** generally have higher baseline survival (0.9776 vs 0.9605)
- **Smoking** has a stronger effect in females (0.7744 vs 0.6012)
- **Age** has a stronger effect in females (0.4648 vs 0.3742)
- **SBP** has a slightly stronger effect in females (0.3131 vs 0.2777)
- **HDL cholesterol** protective effect is similar between sexes

## Implementation Workflow

1. **Calculate uncalibrated risk** using the base formula with model coefficients
2. **Apply regional calibration** using the appropriate scales for the patient's location and sex
3. **Output calibrated percentage** as the final 10-year CVD risk estimate

## Implementation Notes

1. **Input Units**:
   - Age: years
   - SBP: mmHg
   - Total cholesterol: mmol/L
   - HDL cholesterol: mmol/L
   - Smoking: binary (1 = current smoker, 0 = other)

2. **Output**: 10-year CVD risk as a percentage (0-100%)

3. **Model Type**: Cox proportional hazards model with sex-specific coefficients and regional calibration

4. **Default Region**: Belgium (Low Risk region) for initial application development

## Risk Stratification

### Age-Specific Risk Categories

#### Patients <50 years old

- Low to moderate risk: <2.5%
- High risk: 2.5% to <7.5%
- Very high risk: ≥7.5%

#### Patients 50-69 years old

- Low to moderate risk: <5%
- High risk: 5% to <10%
- Very high risk: ≥10%

### Treatment Recommendations

- **Low to moderate risk**: Risk factor treatment plan generally not recommended.
- **High risk**: Risk factor treatment plan should be considered (i.e., blood pressure and LDL-C control).
- **Very high risk**: Risk factor treatment plan should be recommended (i.e., blood pressure and LDL-C control).
