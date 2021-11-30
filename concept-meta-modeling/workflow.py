import json
from pathlib import Path
from typing import Dict
from copy import deepcopy



def get_param_nodes(workflow: Dict):
    return set(
        node_id for node_id, node in workflow.items() if "param" in node.get("key", "")
    )





workflow = json.loads(Path("workflow-data.json").read_text())

workflow_copy = deepcopy(workflow)


# associated to a parametrization node
range_iterator = range(start=0, stop=10, step=1)



for node_id in get_param_nodes(workflow):
    workflow_copy[node_id]["value"] = next(range_iterator)
