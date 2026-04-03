import os
import json
import subprocess

import pytest

pytestmark = pytest.mark.integration

def test_wes_runner_invocation(tmp_path):
    # 🛠️ Set dummy WES environment vars
    env = os.environ.copy()
    env["WES_USER"] = "dummyuser"
    env["WES_PASSWORD"] = "dummypass"
    env["WES_URL"] = "http://localhost:8080"  # or any dummy valid URL

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
        "lenv": {"Identifier": "main", "usid": "test789", "message": "", "cwd": str(tmp_path)},
        "main": {"tmpPath": str(tmp_path)},
        "auth_env": {"user": "testuser"}
    }

    dummy_inputs = {}
    dummy_outputs = {"stac": {"value": None}}

    # Save to temp JSON files
    cwl_path = tmp_path / "cwl.json"
    conf_path = tmp_path / "conf.json"
    inputs_path = tmp_path / "inputs.json"
    outputs_path = tmp_path / "outputs.json"

    for path, data in [(cwl_path, dummy_cwl), (conf_path, dummy_conf), (inputs_path, dummy_inputs), (outputs_path, dummy_outputs)]:
        with open(path, "w") as f:
            json.dump(data, f)

    # Run the main_runner.py with WES
    result = subprocess.run(
        [
            "python3", os.path.abspath(os.path.join(os.path.dirname(__file__), "../main_runner.py")),
            "--runner", "wes",
            "--cwl", str(cwl_path),
            "--conf", str(conf_path),
            "--inputs", str(inputs_path),
            "--outputs", str(outputs_path)
        ],
        capture_output=True,
        text=True,
        env=env  # 👉 Pass env with WES_* values
    )

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    # Check if runner initialized
    assert "Initialized wes runner" in result.stdout
