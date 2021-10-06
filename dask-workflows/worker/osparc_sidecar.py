from simcore_service_sidecar.utils import wrap_async_call
from simcore_service_sidecar.cli import run_sidecar
import simcore_service_sidecar.config as config
from uuid import UUID



print(dir(config))

def run_task(job_id: int, user_id: int, project_id: UUID, node_id: UUID):
    # spawns a docker
    wrap_async_call(run_sidecar(job_id, user_id, project_id, node_id=node_id))