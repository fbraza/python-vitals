import json
from pathlib import Path

import pytest

from vitals.biomarkers import io

INP_FILEPATH = Path(__file__).parent / "inputs"
OUT_FILEPATH = Path(__file__).parent / "outputs"


@pytest.mark.parametrize(
    "input_filename,output_filename",
    [("test__input__patient_01.json", "mobile_output_patient_01.json")],
)
def test_process_json_files(input_filename, output_filename):
    # Process files in the tests directory
    output = io.update(INP_FILEPATH / input_filename)
    with open(OUT_FILEPATH / output_filename) as f:
        expected_result = json.load(f)
        assert output == expected_result
