import json
from pathlib import Path
from typing import Any, TypedDict

from vitals.biomarkers import helpers


class BiomarkerData(TypedDict, total=False):
    """Type definition for processed biomarker data structure."""
    raw_biomarkers: dict[str, Any]


def update(input_file: Path) -> BiomarkerData:
    """Process a single JSON file and create output file with converted biomarkers.

    Args:
        input_file: Path to the input JSON file
    """
    # Load JSON data
    with open(input_file) as f:
        data = json.load(f)

    # Update biomarker names with unit suffixes
    if "raw_biomarkers" in data:
        data["raw_biomarkers"] = helpers.update_biomarker_names(data["raw_biomarkers"])

        # Add converted biomarkers
        data["raw_biomarkers"] = helpers.add_converted_biomarkers(
            data["raw_biomarkers"]
        )

    return data


def write(data: dict[str, Any], output_file: Path) -> None:
    """Write biomarker data to a JSON file.

    Args:
        data: Biomarker data
        output_file: Path to the output JSON file
    """
    # Save output JSON
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Processed: file written at {output_file.name}")


# if __name__ == "__main__":
#     # Process all JSON files in the input directory
#     input_dir = Path("tests/raw")
#     output_dir = Path("tests/inputs")

#     for input_file in input_dir.glob("*.json"):
#         output_file = output_dir / input_file.name.replace("raw", "input")

#         # Update biomarker data
#         data = update(input_file)

#         # Write output file
#         write(data, output_file)
