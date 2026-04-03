import pytest

pytestmark = pytest.mark.integration

ZooCalrissianRunner = pytest.importorskip("zoo_calrissian_runner").ZooCalrissianRunner

DUMMY_CWL = {
    "cwlVersion": "v1.2",
    "$graph": [
        {
            "class": "Workflow",
            "id": "#main",
            "inputs": [],
            "outputs": [],
            "steps": [],
        }
    ],
}

DUMMY_CONF = {
    "lenv": {
        "Identifier": "main",
        "usid": "1234",
        "cwd": ".",
        "message": "",
    },
}


def test_calrissian_runner_instantiation():
    runner = ZooCalrissianRunner(
        cwl=DUMMY_CWL,
        conf=DUMMY_CONF,
        inputs={},
        outputs={},
    )
    assert runner is not None
