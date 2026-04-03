import os

import pytest

pytestmark = pytest.mark.integration

_zoo_wes_runner_mod = pytest.importorskip("zoo_wes_runner.wes_runner")
ZooWESRunner = _zoo_wes_runner_mod.ZooWESRunner

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


@pytest.fixture(autouse=True)
def wes_env_vars():
    os.environ["WES_USER"] = "dummy_user"
    os.environ["WES_PASSWORD"] = "dummy_password"
    os.environ["WES_URL"] = "https://dummy-url.com"


def test_wes_runner_instantiation():
    runner = ZooWESRunner(cwl=DUMMY_CWL, conf=DUMMY_CONF, inputs={}, outputs={})
    assert runner is not None
