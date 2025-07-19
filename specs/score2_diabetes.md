# SCORE2-Diabetes Algorithm Implementation Specification

## Overview

This specification is based on the FORMULA section from the SCORE2-Diabetes calculator. The model calculates 10-year risk of CVD using specific coefficients, baseline survival values, and regional calibration scales.

## Model Coefficients Table

The following coefficients are used to calculate 10-year risk of CVD:

| Risk Factor | Transformation | Male | Female |
|-------------|----------------|------|--------|
| Age, years | cage = (age - 60)/5 | 0.5368 | 0.6624 |
| Smoking | current = 1, other = 0 | 0.4774 | 0.6139 |
| SBP, mm Hg | csbp = (sbp - 120)/20 | 0.1322 | 0.1421 |
| Diabetes | yes = 1, no = 0 | 0.6457 | 0.8096 |
| Total cholesterol, mmol/L | ctchol = tchol - 6 | 0.1102 | 0.1127 |
| HDL cholesterol, mmol/L | chdl = (hdl - 1.3)/0.5 | -0.1087 | -0.1568 |
| Smoking*age interaction | smoking*cage | -0.0672 | -0.1122 |
| SBP*age interaction | csbp*cage | -0.0268 | -0.0167 |
| Diabetes*age interaction | diabetes*cage | -0.0983 | -0.1272 |
| Total cholesterol*age interaction | ctchol*cage | -0.0181 | -0.0200 |
| HDL cholesterol*age interaction | chdl*cage | 0.0095 | 0.0186 |
| Age at diabetes diagnosis, years | cagediab = diabetes*(agediab - 50)/5 | -0.0998 | -0.1180 |
| HbA1c, mmol/mol | ca1c = (a1c - 31)/9.34 | 0.0955 | 0.1173 |
| eGFR | cegfr = (ln(egfr) - 4.5)/0.15 | -0.0591 | -0.0640 |
| eGFR² | cegfr² | 0.0058 | 0.0062 |
| HbA1c*age interaction | ca1c*cage | -0.0134 | -0.0196 |
| eGFR*age interaction | cegfr*cage | 0.0115 | 0.0169 |
| **Baseline survival** | | **0.9605** | **0.9776** |

## Variable Transformations

### Age Transformation
- `cage = (age - 60)/5`

### Systolic Blood Pressure Transformation
- `csbp = (sbp - 120)/20`

### Diabetes Status
- `diabetes = 1` if patient has diabetes, `0` otherwise

### Total Cholesterol Transformation
- `ctchol = tchol - 6`

### HDL Cholesterol Transformation
- `chdl = (hdl - 1.3)/0.5`

### Age at Diabetes Diagnosis Transformation
- `cagediab = diabetes*(agediab - 50)/5`

### HbA1c Transformation
- `ca1c = (a1c - 31)/9.34`

### eGFR Transformations
- `cegfr = (ln(egfr) - 4.5)/0.15`
- `cegfr² = cegfr²` (squared term)

### Smoking Transformation
- `smoking = 1` if current smoker, `0` otherwise

## Initial Risk Calculation Formula

The initial 10-year risk of CVD is calculated using:

```
10-year risk = [1 - (baseline survival)^exp(x)]
```

Where:
- `x = Σ[β*(transformed variables)]`
- The sum includes all coefficients multiplied by their corresponding transformed variables

## Regional Calibration Scales

The region and sex-specific scales to calculate calibrated 10-year risk are as follows:

| Risk Region | Male Scale 1 | Male Scale 2 | Female Scale 1 | Female Scale 2 |
|-------------|--------------|--------------|----------------|----------------|
| Low | -0.5699 | 0.7476 | -0.7380 | 0.7019 |
| Moderate | -0.1565 | 0.8009 | -0.3143 | 0.7701 |
| High | 0.3207 | 0.9360 | 0.5710 | 0.9369 |
| Very high | 0.5836 | 0.8294 | 0.9412 | 0.8329 |

## Calibrated Risk Calculation Formula

The calibrated 10-year risk of CVD is calculated by the following:

```
Calibrated 10-year risk, % = [1 - exp(-exp(scale1 + scale2*ln(-ln(1 - 10-year risk))))] * 100
```

Where:
- `scale1` and `scale2` are the region and sex-specific calibration values from the table above
- `10-year risk` is the initial risk calculated using the baseline survival formula

## Linear Predictor Calculation

The linear predictor (x) is calculated as the sum of:

1. **Main Effects:**
   - Age coefficient × cage
   - Smoking coefficient × smoking
   - SBP coefficient × csbp
   - Diabetes coefficient × diabetes
   - Total cholesterol coefficient × ctchol
   - HDL cholesterol coefficient × chdl
   - Age at diabetes diagnosis coefficient × cagediab
   - HbA1c coefficient × ca1c
   - eGFR coefficient × cegfr
   - eGFR² coefficient × cegfr²

2. **Age Interaction Terms:**
   - Smoking*age coefficient × smoking × cage
   - SBP*age coefficient × csbp × cage
   - Diabetes*age coefficient × diabetes × cage
   - Total cholesterol*age coefficient × ctchol × cage
   - HDL cholesterol*age coefficient × chdl × cage
   - HbA1c*age coefficient × ca1c × cage
   - eGFR*age coefficient × cegfr × cage

## Risk Stratification

### Patients <50 years old
- **Low to moderate risk:** <2.5%
- **High risk:** 2.5% to <7.5%
- **Very high risk:** ≥7.5%

### Patients 50-69 years old
- **Low to moderate risk:** <5%
- **High risk:** 5% to <10%
- **Very high risk:** ≥10%

## Treatment Recommendations

### Low to moderate risk
Risk factor treatment plan generally not recommended.

### High risk
Risk factor treatment plan should be considered (i.e., blood pressure and LDL-C control).

### Very high risk
Risk factor treatment plan should be recommended (i.e., blood pressure and LDL-C control, along with addition of SGLT2-i or GLP1-RA if not already taking).

## Implementation Requirements

### Input Parameters Required
1. Age (years)
2. Sex (Male/Female)
3. Smoking status (current smoker yes/no)
4. Systolic blood pressure (mm Hg)
5. Diabetes status (yes/no)
6. Total cholesterol (mmol/L)
7. HDL cholesterol (mmol/L)
8. Age at diabetes diagnosis (years)
9. HbA1c (mmol/mol)
10. eGFR (estimated glomerular filtration rate)
11. Geographic risk region (Low/Moderate/High/Very high)

### Calculation Steps
1. Transform all input variables using the specified transformations
2. Calculate the linear predictor (x) using sex-specific coefficients
3. Calculate initial 10-year risk using sex-specific baseline survival
4. Apply regional calibration using the calibrated risk formula and region/sex-specific scales
5. Determine risk stratification category based on age and calculated risk percentage
6. Provide appropriate treatment recommendations based on risk category

### Output Requirements
1. **Calibrated 10-year cardiovascular disease risk** as a percentage
2. **Risk stratification category** (Low to moderate/High/Very high)
3. **Treatment recommendation** based on risk category

## Baseline Survival Values

- **Male baseline survival:** 0.9605
- **Female baseline survival:** 0.9776

## Notes
- All coefficients are sex-specific (different values for males and females)
- The model includes both main effects and age interaction terms
- eGFR requires both linear and quadratic terms
- Regional calibration is applied using a two-step process: initial risk calculation followed by regional calibration
- Risk stratification thresholds differ by age group (<50 vs 50-69 years)
- Treatment recommendations are tied directly to risk stratification categories
