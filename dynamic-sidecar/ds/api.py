from fastapi import APIRouter, status, Depends, FastAPI
from fastapi.applications import State

from typing import Dict, Any, Union
from uuid import UUID
from .dependencies import get_app_state


# MODELS ---------------
ContainerId = Union[UUID, str]  # either a name or uuid


# ROUTES ---------------

router = APIRouter(
    prefix="/containers",
    tags=["containers"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Container not found"}},
)


@router.post(
    "",
    responses={
        status.HTTP_201_CREATED: {"description": "Created containers in compose"}
    },
)
def create(compose_file: Dict[str, Any], app_state: State = Depends(get_app_state)):
    """
    - store the docker-compose.yaml (also applies some minimum validation and ensures to avoid naming collisions for container names an network names)
    - pulls images via `docker-compose -p {project} -f {file_path} pull --include-deps`
    """
    print("Validating compose_file")
    # - the compose file (i.e. docker-compose.yaml) shall be already resolved by the director2 and transmitted in json
    #       i.e. the director defines the specs and sends to the worker to execute ... analogously to an orchestra :-)
    # - for validation we HIGHLY recommend to direclyt use 'docker-compose config ...' instead.
    #       We already tried a similar apporach to  utils.validate_compose_spec within pytest_simcore and it is HARD to maintain
    # - Alternatively there is also json-schema https://github.com/compose-spec/compose-spec/blob/master/schema/compose-spec.json
    #
    app_state.compose_file = compose_file
    app_state.container_names = [
        s["container_name"] for s in compose_file["services"].values()
    ]
    try:
        app_state.is_pulling_containers = True

        print("Creating containers ...")
        # docker-compose up ... --no-start
    finally:
        app_state.is_pulling_containers = False


@router.get("")
def list():
    print("docker-compose ps ...")


@router.get("/{id}")
def get(id: ContainerId):
    pass


@router.patch("/{id}", include_in_schema=False)
def update(id: ContainerId):
    # NOT NEEDED
    pass


@router.delete("/{id}", include_in_schema=False)
def delete(id: ContainerId):
    # NOT NEEDED
    pass


@router.post(":up")
def up():
    """
    - start containers via `docker-compose -p {project} -f {file_path} up --no-build -d`
    """
    print("(pull images)")
    print("create containers")
    print("start containers")


@router.post(":down")
def down(keep_compose_file: bool = True, app_state: FastAPI = Depends(get_app_state)):
    """
    - when the service needs to be stopped `docker-compose -p {project} -f {file_path} stop -t {stop_and_remove_timeout}` will be issued with a 5 second timeout to finish all containers after which they will be killed ensuring everything is cleaned up before the dynamic-service gets removed
    """
    print("stop containers")
    print("remove containers")

    if not keep_compose_file:
        app_state.compose_file = None
        app_state.container_names = []


# SUB-RESOURCE LOGS


@router.get("/logs")
def get_container_logs():
    # containerS collection logs
    print("docker-compose logs")


@router.get("/{id}/logs")
def get_container_logs(id: ContainerId):
    # container resouce logs
    print("docker-compose logs {id}")


# ...
