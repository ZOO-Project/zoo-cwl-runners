import importlib
import os
import sys
import argparse
import json
from typing import Dict, Type, Any

# Optional: allow CI (integration job) to inject a deps directory without
# making unit imports heavy. If ZOO_CWL_RUNNERS_DEPS is set, prepend it.
_deps = os.environ.get("ZOO_CWL_RUNNERS_DEPS")
if _deps:
    sys.path.insert(0, _deps)



def load_json(path: str) -> Dict:
    with open(path, 'r') as f:
        return json.load(f)

def select_runner(runner_type: str) -> Type[Any]:
    """
    Lazily import and return the requested runner class.
    Keeps module import cheap so unit tests can import main_runner
    without requiring runner deps to exist in the environment.
    """
    if runner_type == "calrissian":
        mod = importlib.import_module("zoo_calrissian_runner")
        return mod.ZooCalrissianRunner
    elif runner_type == "argowf":
        mod = importlib.import_module("zoo_argowf_runner.runner")
        return mod.ZooArgoWorkflowsRunner
    elif runner_type == "wes":
        mod = importlib.import_module("zoo_wes_runner.wes_runner")
        return mod.ZooWESRunner
    raise ValueError(f"Unsupported runner type: {runner_type}")

# Dummy execution handler for unit testing
class DummyHandler:
    def pre_execution_hook(self): pass
    def post_execution_hook(self, log, output, usage_report, tool_logs): pass
    def get_secrets(self): return None
    def get_additional_parameters(self): return {}
    def get_pod_env_vars(self): return None
    def get_pod_node_selector(self): return None
    def handle_outputs(self, log, output, usage_report, tool_logs): pass
    def set_job_id(self, job_id): pass
    def get_namespace(self): return None
    def get_service_account(self): return None



def main():
    parser = argparse.ArgumentParser(description="Main runner entry point for CWL workflows")
    parser.add_argument("--runner", type=str, required=True, help="Runner type: calrissian, argowf, wes")
    parser.add_argument("--cwl", type=str, required=True, help="Path to CWL file (JSON)")
    parser.add_argument("--conf", type=str, required=True, help="Path to conf file (JSON)")
    parser.add_argument("--inputs", type=str, required=True, help="Path to inputs file (JSON)")
    parser.add_argument("--outputs", type=str, required=True, help="Path to outputs file (JSON)")

    args = parser.parse_args()

    RunnerClass = select_runner(args.runner)

    cwl = load_json(args.cwl)
    conf = load_json(args.conf)
    inputs = load_json(args.inputs)
    outputs = load_json(args.outputs)

    runner = RunnerClass(
        cwl=cwl,
        conf=conf,
        inputs=inputs,
        outputs=outputs,
        execution_handler=DummyHandler(),  # Replace with handler logic if needed
    )

    print(f"Initialized {args.runner} runner")
    result = runner.execute()
    print(f"Execution finished with result: {result}")


if __name__ == "__main__":
    main()
