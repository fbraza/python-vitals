def format_unit_suffix(unit: str) -> str:
    """Convert unit string to a valid suffix format.

    Args:
        unit: Unit string (e.g., "mg/dL", "1000 cells/uL")

    Returns:
        Formatted suffix (e.g., "mg_dl", "1000_cells_ul")
    """
    # Replace special characters with underscores
    suffix = unit.lower()
    suffix = suffix.replace("/", "_")
    suffix = suffix.replace(" ", "_")
    suffix = suffix.replace("^", "")
    return suffix


def update_biomarker_names(biomarkers: dict) -> dict:
    """Update biomarker names to include unit suffixes.

    Args:
        biomarkers: Dictionary of biomarker data with value and unit

    Returns:
        Updated dictionary with unit-suffixed biomarker names
    """
    updated_biomarkers = {}

    for name, data in biomarkers.items():
        if isinstance(data, dict) and "unit" in data:
            unit_suffix = format_unit_suffix(data["unit"])
            new_name = f"{name}_{unit_suffix}"
            updated_biomarkers[new_name] = data
        else:
            # Keep as is if not in expected format
            updated_biomarkers[name] = data

    return updated_biomarkers


def add_converted_biomarkers(biomarkers: dict) -> dict:
    """Add converted biomarker entries for glucose, creatinine, albumin, and CRP.

    Args:
        biomarkers: Dictionary of biomarkers with unit-suffixed names

    Returns:
        Dictionary with original and converted biomarkers
    """
    # Copy original biomarkers
    result = biomarkers.copy()

    # Conversion mappings
    conversions = {
        "glucose_mg_dl": {
            "target_name": "glucose_mmol_l",
            "target_unit": "mmol/L",
            "conversion": lambda x: x / 18.0,
        },
        "glucose_mmol_l": {
            "target_name": "glucose_mg_dl",
            "target_unit": "mg/dL",
            "conversion": lambda x: x * 18.0,
        },
        "creatinine_mg_dl": {
            "target_name": "creatinine_umol_l",
            "target_unit": "umol/L",
            "conversion": lambda x: x * 88.4,
        },
        "creatinine_umol_l": {
            "target_name": "creatinine_mg_dl",
            "target_unit": "mg/dL",
            "conversion": lambda x: x / 88.4,
        },
        "albumin_g_dl": {
            "target_name": "albumin_g_l",
            "target_unit": "g/L",
            "conversion": lambda x: x * 10.0,
        },
        "albumin_g_l": {
            "target_name": "albumin_g_dl",
            "target_unit": "g/dL",
            "conversion": lambda x: x / 10.0,
        },
        "crp_mg_l": {
            "target_name": "crp_mg_dl",
            "target_unit": "mg/dL",
            "conversion": lambda x: x / 10.0,
        },
        "crp_mg_dl": {
            "target_name": "crp_mg_l",
            "target_unit": "mg/L",
            "conversion": lambda x: x * 10.0,
        },
    }

    # Add converted entries
    for source_name, conversion_info in conversions.items():
        if source_name in biomarkers:
            source_value = biomarkers[source_name]["value"]
            target_name = conversion_info["target_name"]

            # Skip if target already exists
            if target_name not in result:
                converted_value = conversion_info["conversion"](source_value)  # type: ignore
                result[target_name] = {
                    "value": round(converted_value, 4),
                    "unit": conversion_info["target_unit"],
                }

    return result
