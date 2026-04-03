import os

import pytest

pytestmark = pytest.mark.integration

_zoo_argowf_runner = pytest.importorskip("zoo_argowf_runner")
ZooArgoWorkflowsRunner = _zoo_argowf_runner.runner.ZooArgoWorkflowsRunner

DUMMY_CWL = {
    "cwlVersion": "v1.0",
    "class": "Workflow",
    "id": "#main",
    "inputs": [],
    "outputs": [],
    "steps": [],
}

DUMMY_CONF = {
    "lenv": {
        "Identifier": "main",
        "usid": "1234",
        "cwd": ".",
        "message": "",
    },
    "auth_env": {"user": "test-user"},
    "main": {"tmpPath": "/tmp"},
}


class DummyExecutionHandler:
    def pre_execution_hook(self):
        pass

    def post_execution_hook(self, log, output, usage_report, tool_logs):
        pass

    def handle_outputs(self, log, output, usage_report, tool_logs):
        pass

    def get_additional_parameters(self):
        return {}

    def get_secrets(self):
        return None

    def get_pod_env_vars(self):
        return None

    def get_pod_node_selector(self):
        return None

    def set_job_id(self, job_id):
        pass


@pytest.fixture(autouse=True)
def runner_env_vars():
    os.environ["STORAGE_CLASS"] = "standard"
    os.environ["DEFAULT_VOLUME_SIZE"] = "10Gi"
    os.environ["DEFAULT_MAX_CORES"] = "4"
    os.environ["DEFAULT_MAX_RAM"] = "4096"


def test_argowf_runner_instantiation():
    runner = ZooArgoWorkflowsRunner(
        cwl=DUMMY_CWL,
        conf=DUMMY_CONF,
        inputs={},
        outputs={},
        execution_handler=DummyExecutionHandler(),
    )
    assert runner is not None
