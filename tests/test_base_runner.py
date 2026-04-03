import pytest
from unittest.mock import MagicMock, patch

pytestmark = pytest.mark.integration

from zoo_runner_common import BaseRunner


class DummyRunner(BaseRunner):
    def wrap(self):
        return self.cwl

    def execute(self):
        return "executed"


DUMMY_CWL = {
    "cwlVersion": "v1.2",
    "class": "Workflow",
    "id": "#main",
    "inputs": {},
    "outputs": {},
    "steps": {},
}

DUMMY_CONF = {
    "lenv": {
        "Identifier": "main",
        "usid": "test-123",
        "message": "",
    },
}


@pytest.fixture
def runner():
    """DummyRunner instance with CWLWorkflow mocked to avoid CWL parsing."""
    with patch("zoo_runner_common.base_runner.CWLWorkflow") as mock_cwl_cls:
        mock_cwl_cls.return_value = MagicMock()
        yield DummyRunner(
            cwl=DUMMY_CWL,
            inputs={},
            conf=DUMMY_CONF,
            outputs={"stac": {"value": None}},
        )


def test_status_update(runner, capsys):
    runner.update_status(10, "testing")
    captured = capsys.readouterr()
    assert "Status 10" in captured.out


def test_log_output(runner, capsys):
    # zoo.info routes through loguru (ZooStub) — just verify it doesn't raise
    runner.log_output({"test": "value"})


def test_execute(runner):
    assert runner.execute() == "executed"


def test_wrap(runner):
    assert runner.wrap() == DUMMY_CWL
