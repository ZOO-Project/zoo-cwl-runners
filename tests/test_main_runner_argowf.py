import os
import json
import subprocess

import pytest

pytestmark = pytest.mark.integration

def test_argowf_runner_invocation(tmp_path):
    # Dummy CWL Workflow JSON
    dummy_cwl = {
        "cwlVersion": "v1.0",
        "class": "Workflow",
        "id": "#main",
        "inputs": [],
        "outputs": [],
        "steps": []
    }

    dummy_conf = {
        "lenv": {"Identifier": "main", "usid": "test123", "message": "", "cwd": str(tmp_path)},
        "main": {"tmpPath": str(tmp_path)},
        "auth_env": {"user": "testuser"}
    }

    dummy_inputs = {}
    dummy_outputs = {"stac": {"value": None}}

    # Save dummy data to temp JSON files
    cwl_path = tmp_path / "cwl.json"
    conf_path = tmp_path / "conf.json"
    inputs_path = tmp_path / "inputs.json"
    outputs_path = tmp_path / "outputs.json"

    for path, data in [
        (cwl_path, dummy_cwl),
        (conf_path, dummy_conf),
        (inputs_path, dummy_inputs),
        (outputs_path, dummy_outputs)
    ]:
        with open(path, "w") as f:
            json.dump(data, f)

    # Call main_runner.py as subprocess
    result = subprocess.run(
        [
            "python3", os.path.abspath(os.path.join(os.path.dirname(__file__), "../main_runner.py")),
            "--runner", "argowf",
            "--cwl", str(cwl_path),
            "--conf", str(conf_path),
            "--inputs", str(inputs_path),
            "--outputs", str(outputs_path)
        ],
        capture_output=True,
        text=True
    )

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    # Assert runner initialized successfully
    assert "Initialized argowf runner" in result.stdout
