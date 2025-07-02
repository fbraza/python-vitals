import json
from pathlib import Path

import helpers


def update(input_file: Path) -> dict:
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


def write(data: dict, output_file: Path) -> None:
    """Write biomarker data to a JSON file.

    Args:
        data: Biomarker data
        output_file: Path to the output JSON file
    """
    # Save output JSON
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Processed: file written at {output_file.name}")


if __name__ == "__main__":
    # Process all JSON files in the input directory
    input_dir = Path("tests/inputs")
    output_dir = Path("tests/outputs")

    for input_file in input_dir.glob("*.json"):
        output_file = output_dir / input_file.name.replace("input", "output")

        # Update biomarker data
        data = update(input_file)

        # Write output file
        write(data, output_file)
