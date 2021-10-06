from dataclasses import dataclass, field
from typing import Callable, Dict

# from dask.distributed import Client
import dask
from dask.delayed import Delayed
from fastapi import APIRouter, FastAPI


def service_executor_core():
    # binds with sidecar functionality
    pass



class ExecutorFactory:
    def create(self, service_name, service_version) -> Callable:
        sevice_metadata = {} # from service_name, service_version

        # TODO: create function with adapted interface, i.e. input/output arguments out based on service_metadata
        # Returned callable is the part that will be serialized to the
        pass

service_executor_factory = ExecutorFactory()




## API resource models ??


@dataclass
class Workflow:
    id: str
    label: str

    pipeline: Dict[str, Delayed] = field(default_factory=dict)

    # - version externally as extension i.e. VersionedWorkflow(Workflow) or a decorator workflow = VersionedWorkflow(workflow, v1)
    # - denoted 'wflow' in short

    @classmethod
    def create(cls, workbench):
        pass

    def update(self, workbench):
        pass


@dataclass
class WorkflowRun:
    id: str
    label: str

    workflow_id: str

    # - a workflow that is or was executed
    # - run state can be observed
    # - denoted 'wrun' in short



## OPERATIONS on resources

async def create_workflow(workbench: Dict) -> Workflow:
    # Parses workbench and converts into a colleciton of dask.Delayed functions
    nouts: Dict[str, Delayed] = {}
    def get_val(v):
        if isinstance(v, dict):
            return nouts[v["nodeUuid"]][v["output"]]
        return v


    for nid, node in workbench.items():
        nins = {name: get_val(value) for name, value in node["inputs"].items()}

        # executor: delayed function

        computational_service_executor = service_executor_factory.create(service_name=node["key"], service_version=node["version"])
        nouts[nid] = dask.delayed(computational_service_executor)(**nins)


    new_flow = Workflow()
    return new_flow


def update_workflow():
    pass


async def start_workflow(workflow_id):
    # dask.Delayed functions can be now submitted to the scheduler
    pass


async def run_workflow(workbench: Dict):
    flow = await create_workflow(workbench)
    run = await start_workflow(workflow_id=flow.id)



# Last layer of API handlers
router = APIRouter()


app = FastAPI()
